import os
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "news.db")
)


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DATABASE_PATH)

def create_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            published TEXT,
            summary TEXT,
            source TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

def get_articles():
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            link,
            published,
            summary,
            source,
            category
        FROM articles
        ORDER BY id DESC
    """)

    articles = cursor.fetchall()

    connection.close()

    return articles

def save_article(article):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO articles (
            title,
            link,
            published,
            summary,
            source,
            category
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        article["title"],
        article["link"],
        article["published"],
        article["summary"],
        article["source"],
        article["category"]
    ))

    inserted = cursor.rowcount == 1

    connection.commit()
    connection.close()

    return inserted

def get_articles_by_source(source):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, published, summary, source, category
        FROM articles
        WHERE source = ?
        ORDER BY id DESC
    """, (source,))

    articles = cursor.fetchall()

    connection.close()

    return articles

def search_articles(search_text):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, published, summary, source, category
        FROM articles
        WHERE title LIKE ? OR summary LIKE ?
        ORDER BY id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    articles = cursor.fetchall()

    connection.close()

    return articles

def get_articles_by_category(category):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, published, summary, source, category
        FROM articles
        WHERE category = ?
        ORDER BY id DESC
    """, (category,))

    articles = cursor.fetchall()

    connection.close()

    return articles