import os
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "news.db")
)

def normalize_existing_dates():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, published
        FROM articles
        WHERE published IS NOT NULL
    """)

    articles = cursor.fetchall()

    for article_id, published in articles:
        if not published:
            continue

        try:
            # Ha már ISO formátumú, nem kell módosítani
            datetime.fromisoformat(published)
            continue
        except ValueError:
            pass

        try:
            date = parsedate_to_datetime(published)

            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)

            normalized = date.astimezone(timezone.utc).isoformat()

            cursor.execute("""
                UPDATE articles
                SET published = ?
                WHERE id = ?
            """, (
                normalized,
                article_id
            ))

        except (TypeError, ValueError):
            print(
                f"Nem sikerült feldolgozni a dátumot: {published}"
            )

    connection.commit()
    connection.close()

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
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_category
        ON articles(category)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_source
        ON articles(source)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_articles_published
        ON articles(published)
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

def filter_articles(search=None, category=None, source=None, period=None, offset=0, limit=20):
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    query = """
        SELECT id, title, link, published, summary, source, category
        FROM articles
        WHERE 1=1
    """

    parameters = []

    if search:
        query += """
            AND (title LIKE ? OR summary LIKE ?)
        """
        parameters.append(f"%{search}%")
        parameters.append(f"%{search}%")

    if category:
        query += """
            AND category = ?
        """
        parameters.append(category)

    if source:
        query += """
            AND source = ?
        """
        parameters.append(source)

    if period:
        now = datetime.now(timezone.utc)

        if period == "today":
            start_date = now - timedelta(days=1)

        elif period == "week":
            start_date = now - timedelta(days=7)

        elif period == "month":
            start_date = now - timedelta(days=30)

        elif period == "year":
            start_date = now - timedelta(days=365)

        else:
            start_date = None

        if start_date:
            query += """
                AND published >= ?
            """
            parameters.append(start_date.isoformat())

    query += """
        ORDER BY published DESC, id DESC
        LIMIT ?
        OFFSET ?
    """

    parameters.append(limit)
    parameters.append(offset)

    cursor.execute(query, parameters)

    articles = cursor.fetchall()

    connection.close()

    return articles

def count_articles(
    search=None,
    category=None,
    source=None,
    period=None
):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM articles
        WHERE 1=1
    """

    parameters = []

    if search:
        query += """
            AND (title LIKE ? OR summary LIKE ?)
        """
        parameters.append(f"%{search}%")
        parameters.append(f"%{search}%")

    if category:
        query += """
            AND category = ?
        """
        parameters.append(category)

    if source:
        query += """
            AND source = ?
        """
        parameters.append(source)

    if period:
        now = datetime.now(timezone.utc)

        if period == "today":
            start_date = now - timedelta(days=1)

        elif period == "week":
            start_date = now - timedelta(days=7)

        elif period == "month":
            start_date = now - timedelta(days=30)

        elif period == "year":
            start_date = now - timedelta(days=365)

        else:
            start_date = None

        if start_date:
            query += """
                AND published >= ?
            """
            parameters.append(start_date.isoformat())

    cursor.execute(query, parameters)

    count = cursor.fetchone()[0]

    connection.close()

    return count

def get_categories():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM articles
        WHERE category IS NOT NULL
        ORDER BY category
    """)

    categories = [
        row[0]
        for row in cursor.fetchall()
    ]

    connection.close()

    return categories

def get_sources():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT DISTINCT source
        FROM articles
        WHERE source IS NOT NULL
        ORDER BY source
    """)

    sources = [
        row[0]
        for row in cursor.fetchall()
    ]

    connection.close()

    return sources