const API_URL = "http://127.0.0.1:5000/detect"; // Your Flask phishing API URL

// Function to send URL to API and check if it's phishing
async function checkURL(url) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    return data.result === "Phishing";
}

// Intercept web requests
chrome.webRequest.onBeforeRequest.addListener(
    async function (details) {
        const isPhishing = await checkURL(details.url);
        if (isPhishing) {
            return { cancel: true }; // Block the request
        }
    },
    { urls: ["<all_urls>"] }, // Monitor all URLs
    ["blocking"] // Enable blocking
);
