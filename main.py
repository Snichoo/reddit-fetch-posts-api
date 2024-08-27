from flask import Flask, request, jsonify
import praw
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Reddit client using credentials from environment variables
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_recent_reddit_posts():
    """Search recent Reddit posts based on keywords provided as a query parameter."""
    keywords = request.args.get('keywords')
    limit = int(request.args.get('limit', 10))  # Default limit is 10 if not provided

    if not keywords:
        return jsonify({"error": "Keywords are required"}), 400

    # Search across all of Reddit
    subreddit = reddit.subreddit("all")
    
    posts = []
    for submission in subreddit.search(keywords, time_filter="hour", sort="new", limit=limit):
        post = {
            "title": submission.title,
            "url": submission.url,
            "content": submission.selftext,
            "submission_id": submission.id,
        }
        posts.append(post)

    return jsonify(posts)

if __name__ == "__main__":
    app.run(debug=True)
