import feedparser
import re

def clean_html(text):
    if not text:
        return ""

    clean_text = re.sub(r"<[^>]+>", "", text)

    return clean_text


def read_rss(rss_url):
    feed = feedparser.parse(rss_url)

    articles = []

    for article in feed.entries:
        news = {
            "title": article.get("title", "Nincs cím"),
            "link": article.get("link", "Nincs link"),
            "published": article.get("published", "Nincs dátum"),
            "summary": article.get("summary", "Nincs leírás")
        }

        articles.append(news)

    return articles