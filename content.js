chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "warnUser") {
        const banner = document.createElement("div");
        banner.style.position = "fixed";
        banner.style.top = "0";
        banner.style.width = "100%";
        banner.style.padding = "10px";
        banner.style.backgroundColor = "#f44336";
        banner.style.color = "#fff";
        banner.style.zIndex = "9999";
        banner.style.textAlign = "center";
        banner.textContent = "⚠️ Warning: This website is flagged as malicious!";
        document.body.appendChild(banner);
    }
});
