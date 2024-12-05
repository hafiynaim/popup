const API_URL = "http://127.0.0.1:5000/phishing-urls"; // Endpoint to fetch phishing URLs

// Function to fetch new phishing URLs and update rules
async function updatePhishingRules() {
    try {
        const response = await fetch(API_URL, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        });

        // Ensure the API response is valid
        if (!response.ok) {
            console.error(
                `Failed to fetch phishing URLs: ${response.status} ${response.statusText}`
            );
            return;
        }

        const phishingURLs = await response.json(); // Assume API returns a list of phishing URLs as JSON

        // Validate the structure of the API response
        if (!Array.isArray(phishingURLs) || phishingURLs.length === 0) {
            console.error("Invalid API response format. Expected a non-empty array of URLs.");
            return;
        }

        // Generate dynamic rules
        const rules = phishingURLs.map((url, index) => ({
            id: index + 1, // Ensure unique rule IDs
            priority: 1,
            action: {
                type: "redirect",
                redirect: {
                    url: chrome.runtime.getURL("blocked.html"),
                },
            },
            condition: {
                urlFilter: url, // Exact URL or pattern
                resourceTypes: ["main_frame"],
            },
        }));

        // Remove existing rules and add the new ones
        chrome.declarativeNetRequest.updateDynamicRules(
            {
                removeRuleIds: rules.map(rule => rule.id), // Remove rules by their IDs
                addRules: rules, // Add new rules
            },
            () => {
                if (chrome.runtime.lastError) {
                    console.error("Error updating rules:", chrome.runtime.lastError.message);
                } else {
                    console.log("Phishing rules successfully updated:", rules);
                }
            }
        );
    } catch (error) {
        console.error("Failed to update phishing rules:", error);
    }
}

// Update rules when the extension starts
updatePhishingRules();

// Listener for extension startup
chrome.runtime.onStartup.addListener(() => {
    console.log("Extension started. Fetching phishing rules...");
    updatePhishingRules();
});

// Listener for installation or update
chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed or updated. Fetching phishing rules...");
    updatePhishingRules();
});
