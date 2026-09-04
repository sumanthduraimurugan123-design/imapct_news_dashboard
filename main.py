import os
import asyncio
import feedparser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "News Dashboard API is running successfully."}

@app.get("/news")
def get_news(category: str = "latest news India", lang: str = "en-IN"):
    encoded_query = category.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={lang}&gl=IN&ceid={lang}"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.get("title", "No Title"),
            "description": entry.get("summary", "No description available"),
            "url": entry.get("link", "#")
        })
    return {"articles": articles}

# Safe event loop initialization for cloud deployment
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)