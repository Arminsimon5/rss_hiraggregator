from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "news.db"


def create_database():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

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


def save_article(article):
    connection = sqlite3.connect(DATABASE_PATH)

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

    connection.commit()
    connection.close()

def get_articles():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, published, summary, source, category
        FROM articles
        ORDER BY id DESC
    """)

    articles = cursor.fetchall()

    connection.close()

    return articles

def get_articles_by_source(source):
    connection = sqlite3.connect(DATABASE_PATH)
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
    connection = sqlite3.connect(DATABASE_PATH)
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
    connection = sqlite3.connect(DATABASE_PATH)
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