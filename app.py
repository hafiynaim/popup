from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load trained model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

@app.route('/detect', methods=['POST'])
def detect_phishing():
    data = request.get_json()
    url = data.get("url", "")

    if not url:
        return jsonify({"result": "Invalid URL"})

    # Vectorize the input URL
    url_vectorized = vectorizer.transform([url])

    # Predict using the loaded model
    prediction = model.predict(url_vectorized)

    # Convert prediction to human-readable format
    result = "Phishing" if prediction[0] == 1 else "Safe"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
