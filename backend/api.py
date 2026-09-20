from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import get_articles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/articles")
def articles():
    rows = get_articles()

    result = []

    for article in rows:
        result.append({
            "id": article["id"],
            "title": article["title"],
            "link": article["link"],
            "published": article["published"],
            "summary": article["summary"],
            "source": article["source"],
            "category": article["category"]
        })

    return result