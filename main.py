from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news")
def get_news(
    role: str = Query("student", description="User role"),
    subcategory: str = Query("School Student", description="Specific subcategory filter"),
    lang: str = Query("en-IN", description="Language code")
):
    # Construct a precise search query string combining role and subcategory
    clean_sub = subcategory.lower().strip()
    query_term = f"{role} {clean_sub}"

    # If you are using a live news provider API key, plug it in here:
    # NEWS_API_KEY = "your_actual_api_key"
    # url = f"https://newsapi.org/v2/everything?q={encodeURIComponent(query_term)}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    # response = requests.get(url)
    # data = response.json()
    # if "articles" in data and data["articles"]:
    #     return {"articles": data["articles"]}

    # Fallback to customized dynamic articles matching the exact chosen subcategory
    personalized_articles = [
        {
            "title": f"Live Updates for {subcategory}: Key Industry & Policy Briefs",
            "description": f"Real-time tracking and breaking reports curated specifically for {role} tracking {subcategory} metrics under language profile {lang}.",
            "url": "https://news.google.com/search?q=" + query_term.replace(" ", "+")
        },
        {
            "title": f"Emerging Trends and Opportunities in {subcategory}",
            "description": f"Critical updates affecting workflow, daily protocols, and advancement guidelines for {role.capitalize()} paths.",
            "url": "https://news.google.com/search?q=" + clean_sub.replace(" ", "+")
        }
    ]

    return {"articles": personalized_articles}