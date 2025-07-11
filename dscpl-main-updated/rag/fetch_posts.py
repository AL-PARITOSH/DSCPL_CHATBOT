# rag/fetch_posts.py

import requests
import json
import os

API_URL = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
HEADERS = {
    "Flic-Token": "flic_b1c6b09d98e2d4884f61b9b3131dbb27a6af84788e4a25db067a22008ea9cce5"
}

def fetch_socialverse_posts(save_path="rag/socialverse_data.json"):
    response = requests.get(API_URL, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()

        # 👇 Check and validate structure
        if "posts" not in data:
            print("[!] 'posts' field not found in response. Raw data preview:")
            print(json.dumps(data, indent=2)[:1000])
            return None

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"[✓] Posts saved to {save_path}")
        return data
    else:
        print(f"[!] Failed to fetch posts. Status code: {response.status_code}")
        return None
