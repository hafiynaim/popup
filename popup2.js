document.getElementById("checkButton").addEventListener("click", async () => {
    const url = document.getElementById("url").value;
    const API_URL = "http://127.0.0.1:5000/detect"; // Your Flask phishing API URL

    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result === "Phishing"
        ? "Phishing URL detected!"
        : "URL is safe.";
});