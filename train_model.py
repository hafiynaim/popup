import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Step 1: Load the dataset
# Replace 'phishing_dataset.csv' with your actual dataset file path
data = pd.read_csv('dataset_phishing.csv')

# Assuming the dataset has two columns: 'url' and 'label'
# 'url' contains the URLs, and 'label' contains 1 for phishing and 0 for safe
urls = data['url']
labels = data['label']

# Step 2: Vectorize the URLs
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(urls)

# Step 3: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Step 4: Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Step 5: Save the model and vectorizer as .pkl files
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model and vectorizer have been saved as 'phishing_model.pkl' and 'vectorizer.pkl'")
