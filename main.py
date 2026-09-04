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

@app.get("/news")
def get_news(
    role: str = Query("student", description="User role"),
    subcategory: str = Query("School Student", description="Specific subcategory filter"),
    lang: str = Query("en-IN", description="Language code")
):
    # Normalize subcategory string for safe matching
    clean_sub = subcategory.lower().strip().replace(" ", "_")
    
    # Comprehensive keyword mapping for all frontend options
    keyword_map = {
        "school_student": "education schools board exams students curriculum",
        "engineering_student": "engineering technology coding students college campus tech",
        "medical_student": "medical entrance NEET healthcare students MBBS hospital",
        "arts_science_student": "university education graduation arts science students degrees",
        "it_tech_professional": "software IT industry technology jobs layoffs AI coding",
        "corporate_executive": "business economy corporate market finance leadership stocks",
        "healthcare_worker": "hospital healthcare medical staff doctors nurses health policy",
        "government_employee": "government schemes policy public sector jobs UPSC administration",
        "voice-first_audio_alerts_only": "breaking news alerts public safety emergency important updates"
    }

    search_query = keyword_map.get(clean_sub, f"{role} {subcategory}")

    # Structured articles payload tailored to the user's role and subcategory
    mock_articles = [
        {
            "title": f"Targeted Update for {role.capitalize()}: {subcategory}",
            "description": f"Essential developments, career updates, and notices regarding {search_query} under language profile {lang}.",
            "url": "https://news.google.com"
        },
        {
            "title": f"Key Policy Analysis Impacting {subcategory}",
            "description": f"Important regulatory shifts and industry trends relevant to {role} professionals.",
            "url": "https://news.google.com"
        }
    ]

    return {"articles": mock_articles}