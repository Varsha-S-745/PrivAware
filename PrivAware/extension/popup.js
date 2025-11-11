
document.getElementById("scanBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    const url = tab.url;

    document.getElementById("risk").innerText = "Scanning...";

    try {
        const res = await fetch("http://localhost:8000/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url })
        });

        const data = await res.json();
        localStorage.setItem("privaware_report", JSON.stringify(data));

        document.getElementById("risk").innerText = "Done ✅";
        const reportPage = chrome.runtime.getURL("report.html");
        document.getElementById("openReport").href = reportPage;
        document.getElementById("openReport").style.display = "block";

    } catch (e) {
        document.getElementById("risk").innerText = "Backend Offline ❌";
    }
});
