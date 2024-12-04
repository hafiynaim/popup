document.getElementById("checkButton").addEventListener("click", async () => {
    const url = document.getElementById("url").value;
    const API_URL = "http://127.0.0.1:5000/detect"; // Replace with your Flask API URL

    // Show a loading message while the request is processed
    const resultElement = document.getElementById("result");
    resultElement.innerText = "Checking URL, please wait...";

    // Send the URL to the Flask API
    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url }),
        });

        if (response.ok) {
            const data = await response.json();
            resultElement.innerText =
                data.result === "Phishing"
                    ? "⚠️ This is a malicious URL!"
                    : "✅ This URL is safe.";
            resultElement.style.color = data.result === "Phishing" ? "red" : "green";
        } else {
            resultElement.innerText = "Error: Unable to process the URL.";
            resultElement.style.color = "orange";
        }
    } catch (error) {
        console.error("Error:", error);
        resultElement.innerText = "Error: Unable to connect to the detection server.";
        resultElement.style.color = "orange";
    }
});
