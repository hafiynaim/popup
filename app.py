from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import joblib

app = Flask(__name__)
CORS(app)

# Load trained model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Route for phishing detection
@app.route('/detect', methods=['POST'])
def detect_phishing():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"result": "Invalid URL"})

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

    if not link:
        return jsonify({'success': False, 'message': 'No link provided.'}), 400

    try:
        with open('dataset_phishing.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([link])
        return jsonify({'success': True, 'message': 'Link added successfully.'})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'success': False, 'message': 'Failed to add link.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
