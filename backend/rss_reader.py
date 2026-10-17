import feedparser
import re
from categorizer import categorize_article
from datetime import datetime, timezone

def clean_html(text):
    if not text:
        return ""

    clean_text = re.sub(r"<[^>]+>", "", text)

    return clean_text

def normalize_date(entry):
    if getattr(entry, "published_parsed", None):
        return datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc
        ).isoformat()

    return None


def read_rss(source_name, rss_url):
    feed = feedparser.parse(rss_url)

    articles = []

    for article in feed.entries:
        title = article.get("title", "Nincs cím")
        summary = clean_html(article.get("summary", ""))

        category = categorize_article(title, summary)

        news = {
            "title": article.get("title", "Nincs cím"),
            "link": article.get("link", "Nincs link"),
            "published": normalize_date(article),
            "summary": clean_html(article.get("summary", "")),
            "source": source_name,
            "category": category
        }

        articles.append(news)

    return articles