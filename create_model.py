from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Sample data
texts = [
    "Great news! Stocks are up",
    "Horrible incident today",
    "Amazing discovery in science",
    "Bad weather ruining plans",
    "Government announces new benefits",
    "Terrorist attack reported",
]
labels = [
    "positive",
    "negative",
    "positive",
    "negative",
    "positive",
    "negative",
]

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = LogisticRegression()
model.fit(X, labels)

# Save
output = {
    'vectorizer': vectorizer,
    'model': model
}

# Make sure model folder exists
os.makedirs('newsapp/model', exist_ok=True)
joblib.dump(output, 'newsapp/model/model.pkl')

print("✅ Model created and saved at newsapp/model/model.pkl")
