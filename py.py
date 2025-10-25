import os
from cerebras.cloud.sdk import Cerebras
import re
from datetime import datetime
import time

# Get API key from GitHub
API_KEY = os.getenv("CEREBRAS_API_KEY")
client = Cerebras(api_key=API_KEY)

USED_KEYWORDS_FILE = "used_keywords.txt"
OUTPUT_FOLDER = "_posts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Your keyword list (keep all of them)
keywords = [
    "best smartphone features for seniors 2025",
    "how long do smartphone batteries last 2025",
    "smartphone accessories every user should have",
    # ... (keep ALL your keywords here)
    "how to fix laptop stuck on manufacturer logo"
]

def load_used_keywords():
    used = set()
    if os.path.exists(USED_KEYWORDS_FILE):
        with open(USED_KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                used.add(line.strip())
    return used

def save_used_keyword(keyword):
    with open(USED_KEYWORDS_FILE, 'a', encoding='utf-8') as f:
        f.write(keyword + '\n')

def generate_blog_post(keyword):
    print(f"Generating: {keyword}")
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "system", "content": f"Write a friendly, helpful blog post about '{keyword}'. 800-1200 words. Use stories, tips, active voice."}],
            model="llama3.1-8b",
            stream=True,
            max_completion_tokens=4000,
            temperature=0.7
        )
        content = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
        return content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""

def format_filename(keyword):
    clean = re.sub(r'[^\w\s-]', '', keyword).strip().lower()
    clean = re.sub(r'\s+', '-', clean)
    date = datetime.now().strftime('%Y-%m-%d')
    return f"{date}-{clean}.md"

def save_post(keyword, content):
    filename = format_filename(keyword)
    path = os.path.join(OUTPUT_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: \"{keyword.title()}\"\n---\n\n{content}")
    print(f"Saved: {filename}")

def main():
    print("Starting Daily Generator...")
    used = load_used_keywords()
    start = time.time()
    max_time = 3600  # 1 hour

    for i, kw in enumerate(keywords, 1):
        if time.time() - start > max_time:
            print("1 hour limit reached.")
            break
        if kw in used:
            print(f"[{i}] SKIP: {kw}")
            continue

        print(f"[{i}] Making: {kw}")
        content = generate_blog_post(kw)
        if content and len(content) > 500:
            save_post(kw, content)
            save_used_keyword(kw)
            print("Done")
        else:
            print("Failed or too short")
        time.sleep(1)

if __name__ == "__main__":
    main()
