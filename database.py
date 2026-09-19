import sqlite3


def create_database():
    connection = sqlite3.connect("news.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            published TEXT,
            summary TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_article(article):
    connection = sqlite3.connect("news.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO articles (
            title,
            link,
            published,
            summary
        )
        VALUES (?, ?, ?, ?)
    """, (
        article["title"],
        article["link"],
        article["published"],
        article["summary"]
    ))

    connection.commit()
    connection.close()

def get_articles():
    connection = sqlite3.connect("news.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, link, published, summary
        FROM articles
        ORDER BY id DESC
    """)

    articles = cursor.fetchall()

    connection.close()

    return articles