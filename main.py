import asyncio
import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from apscheduler.schedulers.background import BackgroundScheduler
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loop = asyncio.get_event_loop()
connected_clients = []

async def event_generator(q: asyncio.Queue):
    try:
        yield f"data: {json.dumps({'title': 'Connected', 'description': 'Live alert stream active'})}\n\n"
        while True:
            try:
                data = await asyncio.wait_for(q.get(), timeout=15.0)
                yield f"data: {json.dumps(data)}\n\n"
            except asyncio.TimeoutError:
                yield f": ping\n\n"
    except asyncio.CancelledError:
        if q in connected_clients:
            connected_clients.remove(q)

@app.get("/news-stream")
async def news_stream():
    q = asyncio.Queue()
    connected_clients.append(q)
    return StreamingResponse(event_generator(q), media_type="text/event-stream")

def background_news_check():
    print("Background Task: Checking for new news updates...")
    rss_url = "https://news.google.com/rss/search?q=latest+news+India&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    if feed.entries:
        latest = feed.entries[0]
        payload = {
            "title": latest.get("title", "No Title"),
            "description": latest.get("summary", "New update available")
        }
        print(f"Broadcasting update: {payload['title']}")
        for client_q in connected_clients:
            asyncio.run_coroutine_threadsafe(client_q.put(payload), loop)

scheduler = BackgroundScheduler()
scheduler.add_job(background_news_check, 'interval', hours=1)
scheduler.start()

@app.get("/trigger-test-alert")
def trigger_test_alert():
    background_news_check()
    return {"status": "Test alert broadcasted to all active browser tabs!"}

@app.get("/news")
def get_news(category: str = "latest news India", lang: str = "en-IN"):
    hl = lang.split('-')[0]
    encoded_query = category.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl={hl}-IN&gl=IN&ceid=IN:{hl}"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.get("title", "No Title"),
            "description": entry.get("summary", "No description available."),
            "url": entry.get("link", "#")
        })
    return {"articles": articles}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)