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
            "title": f"Live Updates 1 for {subcategory}: Key Industry & Policy Briefs",
            "description": f"Real-time tracking and breaking reports curated specifically for {role} tracking {subcategory} metrics under language profile {lang}.",
            "url": "https://news.google.com/search?q=" + query_term.replace(" ", "+")
        },
        {
            "title": f"Emerging Trends and Opportunities in {subcategory}",
            "description": f"Critical updates affecting workflow, daily protocols, and advancement guidelines for {role.capitalize()} paths.",
            "url": "https://news.google.com/search?q=" + clean_sub.replace(" ", "+")
        },
        {
            "title": f"Global Expert Panel Releases New Guidelines for {subcategory}",
            "description": f"Major announcements impacting daily operations and future standards across {role} sectors.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Top Skills and Resources Required for {subcategory} in 2026",
            "description": f"A comprehensive breakdown of tools, training, and certifications recommended for {role} growth.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Advanced Research and Technological Shifts in {subcategory}",
            "description": f"Analyzing breakthrough studies and modern integrations shaping the future of {role} communities.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Regulatory Frameworks and Compliance Updates for {subcategory}",
            "description": f"Essential legal and administrative guidelines every {role} professional must review immediately.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Market Demand and Career Growth Projections for {subcategory}",
            "description": f"Statistical insights and expert forecasting regarding job openings and salary growth metrics.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Case Studies: Successful Implementations in {subcategory}",
            "description": f"Real-world examples highlighting effective operational strategies adopted by leading institutions.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Upcoming Conferences, Workshops, and Webinars for {subcategory}",
            "description": f"A curated calendar of networking events and professional development seminars scheduled for this season.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Future Outlook: What to Expect Next Quarter in {subcategory}",
            "description": f"Strategic planning insights and expert predictions tailored for dedicated {role} stakeholders.",
            "url": "https://news.google.com"
        }
    ]

    return {"articles": personalized_articles}