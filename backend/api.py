import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_database, get_articles, save_article
from rss_reader import read_rss
from sources import RSS_SOURCES


def refresh_all_articles():
    processed = 0
    inserted = 0

    for source in RSS_SOURCES:
        try:
            articles = read_rss(
                source["name"],
                source["url"]
            )

            for article in articles:
                processed += 1

                if save_article(article):
                    inserted += 1

        except Exception as error:
            print(
                f"Hiba az RSS-forrás frissítésekor "
                f"({source['name']}): {error}"
            )

    return {
        "processed": processed,
        "inserted": inserted
    }


async def automatic_refresh():
    while True:
        try:
            result = await asyncio.to_thread(
                refresh_all_articles
            )

            print(
                f"Automatikus RSS frissítés kész: "
                f"{result['processed']} feldolgozva, "
                f"{result['inserted']} új hír."
            )

        except Exception as error:
            print(
                "Automatikus RSS frissítési hiba:",
                error
            )

        await asyncio.sleep(1800)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()

    refresh_task = asyncio.create_task(
        automatic_refresh()
    )

    yield

    refresh_task.cancel()


app = FastAPI(
    root_path="/api",
    lifespan=lifespan
)


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


@app.post("/refresh")
def refresh_articles():
    result = refresh_all_articles()

    return {
        "message": "RSS frissítés kész",
        "processed": result["processed"],
        "inserted": result["inserted"]
    }