from fastapi import FastAPI

from backend.database import get_articles


app = FastAPI()


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