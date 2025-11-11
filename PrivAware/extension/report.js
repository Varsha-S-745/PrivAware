const data = JSON.parse(localStorage.getItem("privaware_report"));
const div = document.getElementById("content");

if (!data) {
    div.innerHTML = "No report found.";
} else {

    // Color coding for risk level
    let levelColor = {
        "SAFE": "green",
        "MODERATE": "orange",
        "RISKY": "red"
    }[data.risk_level] || "black";

    // Format multiline Nmap summary into HTML
    const formatText = (text) => {
        return text.replace(/\n/g, "<br>");
    };

    div.innerHTML = `
      <div class="section">
        <div class="title">Overall Risk Level</div>
        <p style="font-weight:bold; color:${levelColor}">
            ${data.risk_level} (${data.risk_score}/100)
        </p>
      </div>

      <div class="section">
        <div class="title">SSL Analysis</div>
        <p class="desc">Checks if a website’s connection is secure and using HTTPS properly.</p>
        <p>${data.ssl.details}</p>
      </div>

      <div class="section">
        <div class="title">Security Headers</div>
        <p class="desc">Analyzes if the website has essential protection mechanisms enabled.</p>
        <p>${data.headers.details}</p>
      </div>

      <div class="section">
        <div class="title">Third-Party Trackers</div>
        <p class="desc">Detects scripts or tools that collect user data for external companies.</p>
        <p>${data.trackers.details}</p>
      </div>

      <div class="section">
        <div class="title">WHOIS / Domain Info</div>
        <p class="desc">Shows ownership and expiration details of the website.</p>
        <p>${data.whois.details}</p>
      </div>

      <div class="section">
        <div class="title">Open Ports (Nmap)</div>
        <p class="desc">Identifies open network ports and highlights possible security risks.</p>
        <p>${formatText(data.ports.details)}</p>
      </div>
    `;
}
