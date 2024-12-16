Overview
PhishNet Defender is an advanced browser extension designed to detect and block phishing websites in real-time. With its seamless integration, it safeguards users by preventing access to malicious URLs and raising awareness through a phishing simulation tool.

Key Features
🚨 Real-Time Phishing Detection: Automatically blocks phishing websites using an up-to-date database.
🛡️ Dynamic URL Blocking: Leverages Chrome's Declarative Net Request API for efficient rule updates.
🎯 Phishing Simulation Tool: Allows users to test and enhance their phishing awareness.
🌐 User-Friendly Interface: Simple, clean, and intuitive design for all users.
⚡ Lightweight and Fast: Optimized performance without impacting browsing speed.
Technologies Used
JavaScript – Core logic for phishing detection and browser extension functionality
HTML5/CSS3 – Responsive and modern user interface
Python (Flask) – Backend API for phishing URL updates
Chrome Declarative Net Request API – Dynamic rule creation and management
GitHub – Version control and team collaboration
How It Works
The extension fetches phishing URLs from a Flask API.
The URLs are dynamically added to the browser's block list using Chrome's Net Request API.
Users attempting to visit flagged sites are redirected to a warning page.
For awareness, users can also simulate phishing scenarios using the built-in simulation tool.
Setup and Installation
Follow these steps to set up and install the PhishNet Defender extension:

Clone the Repository:

bash
Copy code
git clone https://github.com/hafiynaim/popup.git  
cd PhishNet-Defender  
Load the Extension in Chrome:

Open Chrome and navigate to chrome://extensions/.
Enable Developer Mode (top-right corner).
Click on Load Unpacked and select the cloned project folder.
Run the Flask API (optional):

Contact
For any queries or suggestions:
📧 Email: muhdhafiynaim@gmail.com
👤 Muhammad Hafiy Naim bin Mohd Ismadi
📍 GitHub: github.com/hafiynaim

Happy browsing! Stay safe from phishing 🚨.
