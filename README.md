# AI-based-News-Summarizer-and-Sentiment-Analyzer

🧠 AI-Based News Summarizer & Sentiment Analyzer 📰
This project is an AI/ML-powered web application built using Django that:

Summarizes real-time news articles

Analyzes their sentiment (positive/negative)

Categorizes news by genre and sentiment

Displays top 5 breaking news

Includes a search bar to find specific news articles

🔍 Features
✅ Real-time news fetching using a news API

✂️ Abstractive summarization using Hugging Face’s T5 model

😃 Sentiment analysis using DistilBERT (pre-trained)

🗂️ Categorization by:

Genre (e.g., Sports, Politics, Technology, etc.)

Sentiment (Positive, Negative)

🔝 Top 5 breaking news panel

🔎 Search functionality for user-defined queries

🌐 Built with HTML/CSS + Django Templates

🧰 Tech Stack
Backend: Django (Python)

Frontend: HTML, CSS (Django templates)

AI/ML Models:

t5-small for summarization

distilbert-base-uncased-finetuned-sst-2-english for sentiment

APIs: NewsAPI.org (or similar for fetching news)

🎯 Goals
To demonstrate the integration of AI/ML models in a real-world web application

To showcase NLP capabilities like summarization and sentiment detection

To provide an interactive and intelligent news portal


📁File Structure

news_aiml_project/

├── news_aiml_project/

│   └── settings.py, urls.py, wsgi.py

├── newsapp/

│   ├── templates/

│   │   ├── index.html

│   │   └── result.html

│   ├── static/

│   ├── ml_models/

│   │   ├── summarizer_model.py

│   │   └── sentiment_model.py

│   ├── utils.py

│   ├── views.py

│   └── urls.py

├── manage.py

└── requirements.txt



📷Screenshots
![Screenshot 2025-05-13 144011](https://github.com/user-attachments/assets/f4efc5e9-878e-4db4-8abc-ecc652576bef)

![Screenshot 2025-05-13 222725](https://github.com/user-attachments/assets/d470fe2a-aafa-4e56-9a7c-6e7c6a62586f)


