import praw
import os
import json

# Load your Reddit API keys from environment or config
REDDIT_CLIENT_ID = 'NrcctWyVhJOKtS4VELIAYQ'
REDDIT_CLIENT_SECRET = 'gbJnGsHUK38xt_VG6DAeE0BaJI4pSw'
REDDIT_USER_AGENT = 'PersonaScraper/0.1'

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def scrape_user(username: str, limit=200) -> dict:
    try:
        user = reddit.redditor(username)

        profile_data = {
            "username": username,
            "comment_karma": user.comment_karma,
            "link_karma": user.link_karma,
            "created_utc": user.created_utc
        }

        comments = []
        for comment in user.comments.new(limit=limit):
            comments.append({
                "body": comment.body,
                "score": comment.score,
                "subreddit": str(comment.subreddit),
                "permalink": f"https://reddit.com{comment.permalink}",
                "created_utc": comment.created_utc
            })

        posts = []
        for post in user.submissions.new(limit=limit):
            posts.append({
                "title": post.title,
                "selftext": post.selftext,
                "score": post.score,
                "subreddit": str(post.subreddit),
                "permalink": f"https://reddit.com{post.permalink}",
                "created_utc": post.created_utc
            })

        return {
            "profile": profile_data,
            "comments": comments,
            "posts": posts
        }

    except Exception as e:
        return {"error": str(e)}

def save_user_data(username: str, data: dict, output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/{username}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

