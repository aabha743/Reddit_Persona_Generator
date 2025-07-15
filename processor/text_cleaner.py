import re
import json
import os

def clean_text(text: str) -> str:
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    # Remove emojis
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove markdown formatting (basic)
    text = re.sub(r'\*|\_|~|`|>|#+', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_user_data(raw_data: dict) -> dict:
    cleaned = {
        "username": raw_data.get("profile", {}).get("username", "unknown"),
        "profile": raw_data.get("profile", {}),
        "comments": [],
        "posts": []
    }

    for comment in raw_data.get("comments", []):
        cleaned["comments"].append({
            "cleaned_body": clean_text(comment["body"]),
            **comment
        })

    for post in raw_data.get("posts", []):
        full_text = post["title"] + " " + post["selftext"]
        cleaned["posts"].append({
            "cleaned_text": clean_text(full_text),
            **post
        })

    return cleaned

def save_cleaned_data(username: str, data: dict, output_dir="data/cleaned"):
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/{username}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

