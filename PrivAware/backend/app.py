from fastapi import FastAPI
from pydantic import BaseModel
import ssl, socket, whois, subprocess, shutil, urllib.parse, time

app = FastAPI()

class Req(BaseModel):
    url: str
def check_ssl(host):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(4)
            s.connect((host, 443))
        return {"details": "✅ Valid SSL certificate detected."}
    except Exception as e:
        return {"details": f"❌ SSL certificate missing or invalid."}

def check_headers(url):
    import requests
    try:
        r = requests.get(url, timeout=5)
        missing = []
        needed = ["Content-Security-Policy", "X-Frame-Options", "X-XSS-Protection"]
        for h in needed:
            if h not in r.headers:
                missing.append(h)

        if missing:
            return {"details": f"⚠ Missing security headers: {', '.join(missing)}."}
        else:
            return {"details": "✅ Strong security headers present."}
    except:
        return {"details": "❌ Could not fetch headers."}

def check_trackers(url):
    import requests
    try:
        text = requests.get(url, timeout=5).text
        risky = [
            "google-analytics", "tracker", "facebook", "advert",
            "googletagmanager", "doubleclick"
        ]
        found = [k for k in risky if k in text.lower()]
        if found:
            return {"details": f"⚠ Trackers found: {', '.join(found)}."}
        return {"details": "✅ No major trackers detected."}
    except:
        return {"details": "❌ Could not scan for trackers."}

def check_whois(host):
    try:
        info = whois.whois(host)
        if getattr(info, "expiration_date", None):
            return {"details": "✅ Domain WHOIS available."}
        return {"details": "⚠ WHOIS available but incomplete."}
    except:
        return {"details": "❌ WHOIS lookup failed."}
def parse_nmap_output(op):
    """
    Converts Nmap text into user-friendly summary.
    """
    summary = {
        "open_ports": [],
        "risk": []
    }

    lines = op.split("\n")
    for line in lines:
        if "/tcp" in line and ("open" in line):
            parts = line.split()
            port = parts[0]
            service = parts[-1]
            summary["open_ports"].append(f"{port} ({service})")

            p = int(port.split("/")[0])
            if p in [21, 22, 23, 110, 143, 3306, 8080]:
                summary["risk"].append(f"⚠ Port {p} is commonly targeted.")

    if not summary["open_ports"]:
        return "✅ No risky ports detected."

    readable = "🔍 Open Ports Detected:\n" + "\n".join(
        [f"• {p}" for p in summary["open_ports"]]
    )

    if summary["risk"]:
        readable += "\n\nPotential Risks:\n" + "\n".join(
            [f"• {r}" for r in summary["risk"]]
        )
    else:
        readable += "\n\n✅ No risky ports found."

    return readable


def check_ports(host):
    nmap_path = shutil.which("nmap")
    if not nmap_path:
        return {"details": "❌ Nmap is not installed on the server."}

    try:
        proc = subprocess.run(
            [nmap_path, "-F", host],
            capture_output=True,
            text=True,
            timeout=60
        )
        raw = proc.stdout or proc.stderr
        summary = parse_nmap_output(raw)
        return {"details": summary}
    except subprocess.TimeoutExpired:
        return {"details": "❌ Nmap scan timed out."}
    except Exception:
        return {"details": "❌ Nmap scan failed."}

@app.post("/scan")
def scan(data: Req):
    url = data.url
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        return {"error": "Invalid URL provided"}

    ssl_res = check_ssl(host)
    headers_res = check_headers(url)
    trackers_res = check_trackers(url)
    whois_res = check_whois(host)
    ports_res = check_ports(host)

    score = 0
    if "❌" in ssl_res["details"]: score += 25
    if "⚠" in headers_res["details"]: score += 20
    if "⚠" in trackers_res["details"]: score += 15
    if "❌" in whois_res["details"]: score += 10
    if "⚠" in ports_res["details"]: score += 25

    level = "SAFE"
    if score > 40: level = "MODERATE"
    if score > 70: level = "RISKY"

    return {
        "risk_score": score,
        "risk_level": level,
        "ssl": ssl_res,
        "headers": headers_res,
        "trackers": trackers_res,
        "whois": whois_res,
        "ports": ports_res,
        "scanned_at": time.time()
    }
