import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Example dummy training data
text_data = [
    "Good news about economy",
    "Bad news about war",
    "Exciting sports event",
    "Terrible weather forecast",
    "Neutral update on stock market"
]
labels = ["positive", "negative", "positive", "negative", "neutral"]

# 2. Initialize vectorizer
vectorizer = TfidfVectorizer()

# 3. Vectorize the text data
X = vectorizer.fit_transform(text_data)

# 4. Initialize and train the model
model = LogisticRegression()
model.fit(X, labels)

# 5. Save the model and vectorizer
joblib.dump(model, 'model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("✅ Model and vectorizer saved successfully!")
