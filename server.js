const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000; // Define your backend port

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Route to handle suspicious link submissions
app.post('/submit-link', (req, res) => {
  const { link } = req.body;

  if (!link) {
    return res.status(400).json({ success: false, message: 'No link provided' });
  }

  console.log(`Received suspicious link: ${link}`);
  
  // Placeholder: You can add logic here to save the link to a database, analyze it, or log it.
  // For now, just return a success response.
  return res.status(200).json({ success: true, message: 'Link submitted successfully' });
});

// Server Listening
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
