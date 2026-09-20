from backend.rss_reader import read_rss
from backend.database import create_database, save_article, get_articles, get_articles_by_category, get_articles_by_source, search_articles
from backend.sources import RSS_SOURCES


create_database()


for source in RSS_SOURCES:

    print("Beolvasás:", source["name"])

    try:
        articles = read_rss(
            source["name"],
            source["url"]
        )

        for article in articles:
            save_article(article)

        print("Sikeres beolvasás:", len(articles), "hír")

    except Exception as error:
        print("Hiba a forrás beolvasásakor:", error)


print()
print("Hírek elmentve.")
print()


saved_articles = get_articles()

for article in saved_articles:
    print("Forrás:", article["source"])
    print("Kategória:", article["category"])
    print("Cím:", article["title"])
    print("Link:", article["link"])
    print("Dátum:", article["published"])
    print("Leírás:", article["summary"])
    print("-" * 50)