from rss_reader import read_rss
from database import create_database, save_article, get_articles


rss_url = "https://www.vezess.hu/feed/"

create_database()

articles = read_rss(rss_url)

for article in articles:
    save_article(article)

saved_articles = get_articles()

for article in saved_articles:
    print("ID:", article["id"])
    print("Cím:", article["title"])
    print("Link:", article["link"])
    print("Dátum:", article["published"])
    print("Leírás:", article["summary"])
    print("-" * 50)