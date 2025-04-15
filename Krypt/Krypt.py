from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from pycoingecko import CoinGeckoAPI
import feedparser
import praw
import requests
import re
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes and origins
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"]}})

# Initialize APIs
cg = CoinGeckoAPI()
analyzer = SentimentIntensityAnalyzer()

[Previous code remains the same...]

if __name__ == '__main__':
    print(" * Starting Crypto Sentiment Analysis Server...")
    print(" * Server is running at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)