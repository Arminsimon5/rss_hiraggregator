import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_database, filter_articles, save_article, normalize_existing_dates, count_articles, get_categories, get_sources
from sources import RSS_SOURCES
from rss_reader import read_rss


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
    normalize_existing_dates()

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
def articles(
    search: str | None = None,
    category: str | None = None,
    source: str | None = None,
    period: str | None = None,
    limit: int = 20,
    offset: int = 0
):
    rows = filter_articles(
        search=search,
        category=category,
        source=source,
        period=period,
        limit=limit,
        offset=offset
    )
    
    total = count_articles(
        search=search,
        category=category,
        source=source,
        period=period
    )

    items = []

    for article in rows:
        items.append({
            "id": article["id"],
            "title": article["title"],
            "link": article["link"],
            "published": article["published"],
            "summary": article["summary"],
            "source": article["source"],
            "category": article["category"]
        })

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }

    
@app.post("/refresh")
def refresh_articles():
    result = refresh_all_articles()

    return {
        "message": "RSS frissítés kész",
        "processed": result["processed"],
        "inserted": result["inserted"]
    }

@app.get("/categories")
def categories():
    return get_categories()


@app.get("/sources")
def sources():
    return get_sources()