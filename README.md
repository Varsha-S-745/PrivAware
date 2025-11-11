# 🚨 PrivAware Lite — Website Privacy & Security Risk Analyzer (Chrome Extension)

PrivAware Lite is a Chrome extension that analyzes any website for privacy risks, security misconfigurations, and potential vulnerabilities.  
It uses a **Python FastAPI backend** to perform real-time checks like SSL validation, security headers analysis, WHOIS lookup, tracker detection, and optional Nmap scanning.

---

## ✅ Features

- SSL/TLS certificate validation  
- HTTP security headers analysis  
- WHOIS domain information  
- Third-party tracker detection  
- Optional Nmap port scanning  
- Simple risk scoring and readable reports inside the extension

---

## 📥 Download & Run (Step-by-step)

You can run PrivAware locally in two ways: **native Python** (recommended for development). The extension expects the backend at `http://localhost:8000/scan` by default. If you run the backend on a different port, update the extension fetch URL accordingly.

1. **Get the project**
   - From GitHub:
     ```bash
     git clone https://github.com/Varsha S/PrivAware-Lite.git
     cd PrivAware-Lite
     ```
   - Or download the ZIP from GitHub and extract it.

2. **Open a terminal and go to the backend folder**
   ```bash
   cd Backend
   uvicorn app:app --reload --port 8000
   ```
3. Go to chrome click extension-  manage extension
4. click developer mode and clcicl load unpacked
5. choose privaware and click extension
6. open any website and open the extension , it sows report correctly this readme file formationg is not frmal make it formal**
