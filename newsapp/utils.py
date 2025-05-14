# newsapp/utils.py

import requests
from .ml_models.summarizer_model import summarize_text
from .ml_models.sentiment_model import predict_sentiment

# Your NewsAPI key (you have to get your own free API key from https://newsapi.org)
NEWS_API_KEY = "f94592e68303446aac394df5b8dedb97"

# Fetch news from NewsAPI
# def fetch_news(query=None):
#     """Fetch latest news articles."""
#     base_url = "https://newsapi.org/v2/top-headlines"
#     params = {
#         "apiKey": NEWS_API_KEY,
#         "country": "in",  # You can change to 'us' or any country
#         "pageSize": 20,
#     }
#     if query:
#         params["q"] = query

#     response = requests.get(base_url, params=params)
#     data = response.json()
#     articles = data.get('articles', [])
#     return articles

# newsapp/utils.py

def fetch_news(query=""):
    """Fetch news articles from NewsAPI."""
    api_key = "YOUR_NEWS_API_KEY_HERE"
    url = f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={api_key}"
    
    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "ok":
        return data["articles"]  # Return list of articles
    else:
        return []



# Genre Categorization based on keywords
def categorize_genre(title, description):
    """Simple genre categorization based on keywords."""
    text = (title + " " + description).lower()
    if any(keyword in text for keyword in ["politics", "election", "government"]):
        return "Politics"
    elif any(keyword in text for keyword in ["sports", "match", "tournament"]):
        return "Sports"
    elif any(keyword in text for keyword in ["business", "economy", "finance", "market"]):
        return "Business"
    elif any(keyword in text for keyword in ["technology", "tech", "startup", "software"]):
        return "Technology"
    elif any(keyword in text for keyword in ["health", "medicine", "covid", "vaccine"]):
        return "Health"
    elif any(keyword in text for keyword in ["entertainment", "movie", "film", "music", "show"]):
        return "Entertainment"
    else:
        return "General"

# Process News: Summarize, Analyze Sentiment, Categorize
# def process_news(articles):
#     """Process each news article: summarize, sentiment, genre."""
#     processed_articles = []

#     for article in articles:
#         title = article.get('title', '')
#         description = article.get('description', '')
#         content = article.get('content', '')
#         url = article.get('url', '')
#         image_url = article.get('urlToImage', '')
#         published_at = article.get('publishedAt', '')

#         full_text = title + ". " + (description if description else content)

#         if not full_text.strip():
#             continue  # skip empty articles

#         try:
#             summary = summarize(full_text)
#         except Exception as e:
#             summary = "Summary not available."

#         try:
#             sentiment, confidence = predict_sentiment(summary)
#         except Exception as e:
#             sentiment = "Neutral"
#             confidence = 0.5

#         genre = categorize_genre(title, description)

#         processed_articles.append({
#             "title": title,
#             "summary": summary,
#             "sentiment": sentiment,
#             "confidence": round(confidence * 100, 2),
#             "genre": genre,
#             "url": url,
#             "image_url": image_url,
#             "published_at": published_at,
#         })

#     return processed_articles

def process_news(articles):
    """Process the fetched articles, including summarization and sentiment analysis."""
    processed_articles = []
    for article in articles:
        # Summarize the article
        summary = summarize_text(article['description'])
        
        # Sentiment analysis
        sentiment, confidence = predict_sentiment(summary)
        
        # Prepare the processed article
        processed_article = {
            'title': article['title'],
            'summary': summary,
            'sentiment': sentiment,
            'confidence': confidence,
            'published_at': article['publishedAt'],
            'url': article['url'],
            'image_url': article.get('urlToImage', None),
            'genre': article['category'],  # Assuming category is available
        }
        
        processed_articles.append(processed_article)
    
    return processed_articles
