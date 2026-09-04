from fastapi import FastAPI, Query
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
def home():
    return {"message": "Impact News Dashboard API is running successfully!"}

@app.get("/news")
def get_news(
    role: str = Query("student", description="User role"),
    subcategory: str = Query("School Student", description="Specific subcategory filter"),
    lang: str = Query("en-IN", description="Language code")
):
    clean_sub = subcategory.lower().strip()
    query_term = f"{role} {clean_sub}"

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