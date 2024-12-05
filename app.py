from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import joblib
import bcrypt
import sqlite3
import os
import validators

app = Flask(__name__)
CORS(app)

# Load trained model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Ensure CSV file exists
if not os.path.exists('dataset_phishing.csv'):
    with open('dataset_phishing.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL'])

# Database setup (SQLite example)
def init_db():
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL
                     )''')
        conn.commit()

# Validate email and password input
def validate_email(email):
    if not email or not validators.email(email):
        return False
    return True

def validate_password(password):
    # Password should have a minimum length of 8 characters
    # and include at least one digit and one special character
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
        return False
    return True

# Route for phishing detection
@app.route('/detect', methods=['POST'])
def detect_phishing():
    data = request.get_json()
    url = data.get("url", "")

    if not url or not validators.url(url):
        return jsonify({"result": "Invalid URL format"}), 400

    try:
        # Vectorize the input URL
        url_vectorized = vectorizer.transform([url])

        # Predict using the loaded model
        prediction = model.predict(url_vectorized)

        # Convert prediction to human-readable format
        result = "Phishing" if prediction[0] == 1 else "Safe"

        return jsonify({"result": result})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"result": "Error during prediction"}), 500

# Route for submitting links to a CSV file
@app.route('/submit-link', methods=['POST'])
def submit_link():
    data = request.json
    link = data.get('link')

    if not link or not validators.url(link):
        return jsonify({'success': False, 'message': 'Invalid link provided.'}), 400

    try:
        with open('dataset_phishing.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([link])
        return jsonify({'success': True, 'message': 'Link added successfully.'})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'Failed to add link.'}), 500

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Input validation
        if not username:
            return jsonify({'success': False, 'message': 'Username is required!'}), 400

        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format!'}), 400

        if not validate_password(password):
            return jsonify({'success': False, 'message': 'Password must be at least 8 characters long, include a digit, and a special character.'}), 400

        # Encrypt the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store the user in the database
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, hashed_password.decode('utf-8')))
            conn.commit()

        return jsonify({'success': True, 'message': 'Account created successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during sign-up.'}), 500

# Login Route
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format!'}), 400

        if not password:
            return jsonify({'success': False, 'message': 'Password is required!'}), 400

        # Fetch user from the database
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            result = c.fetchone()

            if not result:
                return jsonify({'success': False, 'message': 'User not found!'}), 404

            stored_password = result[0]

        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Incorrect password!'}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during login.'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
