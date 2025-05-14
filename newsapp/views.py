import json
import os
import joblib
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from transformers import pipeline


# Load model and vectorizer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_data = joblib.load(os.path.join(BASE_DIR, 'newsapp', 'model', 'model.pkl'))

if isinstance(model_data, dict):
    model = model_data.get('model')
    vectorizer = model_data.get('vectorizer')
else:
    model = model_data
    vectorizer = joblib.load(os.path.join(BASE_DIR, 'newsapp', 'model', 'vectorizer.pkl'))  # fallback

# API Configuration
NEWS_API_KEY = 'Your_Api_key'
NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

# Initialize Huggingface Sentiment Pipeline
# sentiment_pipeline = pipeline("sentiment-analysis")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

summarizer_pipeline = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)
# Simple genre categorization based on keywords
def categorize_article(title, description):
    keywords = {
        'Sports': ['football', 'soccer', 'basketball', 'cricket', 'tennis', 'sports'],
        'Politics': ['election', 'president', 'government', 'policy', 'politics', 'senate', 'law'],
        'Technology': ['tech', 'technology', 'software', 'gadget', 'AI', 'robot', 'computer'],
        'Entertainment': ['movie', 'music', 'actor', 'celebrity', 'tv', 'show'],
        'Business': ['business', 'market', 'stock', 'finance', 'economy', 'startup'],
        'Health': ['covid', 'vaccine', 'health', 'doctor', 'hospital', 'disease', 'medicine'],
        'Science': ['science', 'research', 'space', 'nasa', 'discovery', 'experiment'],
    }

    text = (title + " " + description).lower()
    for genre, words in keywords.items():
        if any(word in text for word in words):
            return genre
    return "General"


# summarizer_pipeline = pipeline("summarization")

# Summarize function using transformers
# def summarize_text(text):
#     if not text or len(text.split()) < 50:
#         return text  # Too short, no need to summarize
#     try:
#         summary = summarizer_pipeline(text, max_length=70, min_length=50, do_sample=False)[0]['summary_text']
#         return summary
#     except:
#         return text  # fallback

def summarize_text(text):
    if not text:
        return "No content to summarize."

    word_count = len(text.split())

    # Don't summarize very short texts
    if word_count < 40:
        return text

    # Use a proportional max_length, ensure it's more than min_length
    max_len = min(120, int(word_count * 0.8))  # Cap at 120 tokens
    min_len = max(30, int(word_count * 0.4))   # Ensure a base summary size

    try:
        summary = summarizer_pipeline(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return text  # Fallback to original



def get_sentiment(text):
    result = sentiment_pipeline(text)[0]
    return result['label']

# def index(request):
#     query = request.GET.get('query')
#     if query:
#         url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
#     else:
#         url = NEWS_API_URL

#     response = requests.get(url)
#     articles = []
#     if response.status_code == 200:
#         data = response.json()
#         articles = data.get('articles', [])
#         for article in articles:
#             title = article.get('title') or ""
#             description = article.get('description') or ""

#             article['genre'] = categorize_article(title, description)
#             article['summary'] = summarize_text(description)
    
#     return render(request, 'index.html', {'articles': articles, 'query': query})
# def index(request):
#     query = request.GET.get('query')
#     genre = request.GET.get('genre')

#     genre_keywords = {
#         'Sports': 'sports',
#         'Politics': 'politics',
#         'Technology': 'technology',
#         'Entertainment': 'entertainment',
#         'Business': 'business',
#         'Health': 'health',
#         'Science': 'science'
#     }

#     if query:
#         url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
#     elif genre and genre in genre_keywords:
#         url = f'https://newsapi.org/v2/everything?q={genre_keywords[genre]}&apiKey={NEWS_API_KEY}'
#     else:
#         url = NEWS_API_URL

#     response = requests.get(url)
#     articles = []
#     if response.status_code == 200:
#         data = response.json()
#         articles = data.get('articles', [])[:6]
#         for article in articles:
#             title = article.get('title') or ""
#             # description = article.get('description') or ""
#             description = article.get('description') or ""
#             content = article.get('content') or ""
#             full_text = description + " " + content

#             article['genre'] = categorize_article(title, description)
#             # article['summary'] = summarize_text(description)
#             article['summary'] = summarize_text(full_text)


#     return render(request, 'index.html', {
#         'articles': articles,
#         'query': query,
#         'genre': genre
#     })
from django.core.cache import cache  # Make sure this is imported at the top

def index(request):
    query = request.GET.get('query')
    genre = request.GET.get('genre')

    genre_keywords = {
        'Sports': 'sports',
        'Politics': 'politics',
        'Technology': 'technology',
        'Entertainment': 'entertainment',
        'Business': 'business',
        'Health': 'health',
        'Science': 'science'
    }

    # Build a cache key based on query or genre
    cache_key = f"news_{query or genre or 'default'}"
    articles = cache.get(cache_key)

    if not articles:
        if query:
            url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
        # elif genre and genre in genre_keywords:
        #     url = f'https://newsapi.org/v2/everything?q={genre_keywords[genre]}&apiKey={NEWS_API_KEY}'
        # else:
        #     url = NEWS_API_URL
        elif genre and genre != "All" and genre in genre_keywords:
            url = f'https://newsapi.org/v2/everything?q={genre_keywords[genre]}&apiKey={NEWS_API_KEY}'
        else:
            url = NEWS_API_URL  # Use top headlines when 'All' is selected


        response = requests.get(url)
        articles = []
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:6]
            for article in articles:
                title = article.get('title') or ""
                description = article.get('description') or ""
                content = article.get('content') or ""
                full_text = description + " " + content

                article['genre'] = categorize_article(title, description)
                article['summary'] = summarize_text(full_text)

            # Save to cache for 120 minutes
            cache.set(cache_key, articles, timeout=7200)

    return render(request, 'index.html', {
        'articles': articles,
        'query': query,
        'genre': genre
    })





def predict(request):
    if request.method == 'GET':
        news_text = request.GET.get('news_text')
        if news_text:
            text_vector = vectorizer.transform([news_text])
            prediction = model.predict(text_vector)[0]
            return render(request, 'result.html', {'prediction': prediction})
    return redirect('/')

@csrf_exempt
def predict_ajax(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            text = data.get('text')

            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)

            text_vector = vectorizer.transform([text])
            prediction = model.predict(text_vector)[0]
            sentiment = get_sentiment(text)

            return JsonResponse({
                'prediction': prediction,
                'sentiment': sentiment
            })
        except Exception as e:
            print(f"Error in predict_ajax: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
