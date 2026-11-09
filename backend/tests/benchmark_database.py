import os
import sqlite3
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_NO_INDEX = BASE_DIR / "benchmark_no_index.db"
DATABASE_INDEXED = BASE_DIR / "benchmark_indexed.db"


def create_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS articles
    """)

    cursor.execute("""
        CREATE TABLE articles (
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

def create_indexes(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

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

def measure_all(database_path):
    results = {}

    results["Összes hír"] = measure_query(
        database_path,
        "Összes hír",
        """
        SELECT *
        FROM articles
        ORDER BY published DESC
        """
    )

    results["Keresés"] = measure_query(
        database_path,
        "Keresés",
        """
        SELECT *
        FROM articles
        WHERE title LIKE ?
           OR summary LIKE ?
        """,
        ("%Mazda%", "%Mazda%")
    )

    results["Kategória szűrés"] = measure_query(
        database_path,
        "Kategória szűrés",
        """
        SELECT *
        FROM articles
        WHERE category = ?
        """,
        ("Motorsport",)
    )

    results["Forrás szűrés"] = measure_query(
        database_path,
        "Forrás szűrés",
        """
        SELECT *
        FROM articles
        WHERE source = ?
        """,
        ("Vezess",)
    )

    results["Időszűrés"] = measure_query(
        database_path,
        "Időszűrés",
        """
        SELECT *
        FROM articles
        WHERE published >= ?
        """,
        ("2026-11-01T00:00:00+00:00",)
    )

    results["Lapozás 20 rekord"] = measure_query(
        database_path,
        "Lapozás 20 rekord",
        """
        SELECT *
        FROM articles
        ORDER BY published DESC
        LIMIT 20 OFFSET 0
        """
    )

    return results


def insert_test_data(database_path, count):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    articles = []

    categories = [
        "Elektromos autók",
        "Motorsport",
        "Autótesztek",
        "Új autók",
        "Tuning",
        "Közlekedés",
        "Egyéb"
    ]

    sources = [
        "Vezess",
        "Autonavigator",
        "Autó-Motor",
        "Autópult",
        "Villanyautosok",
        "Racingline",
        "E-Cars",
        "Alapjárat"
    ]

    for i in range(count):
        articles.append((
            f"Teszt hír {i}",
            f"https://example.com/article/{i}",
            "2026-11-08T12:00:00+00:00",
            f"Ez a {i}. teszt hír összefoglalója Mazda elektromos autó témában.",
            sources[i % len(sources)],
            categories[i % len(categories)]
        ))

    cursor.executemany("""
        INSERT INTO articles (
            title,
            link,
            published,
            summary,
            source,
            category
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, articles)

    connection.commit()
    connection.close()


def measure_query(
    database_path,
    name,
    query,
    parameters=(),
    repetitions=30
):
    times = []

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Bemelegítő lekérdezés
    cursor.execute(query, parameters)
    cursor.fetchall()

    for _ in range(repetitions):
        start = time.perf_counter()

        cursor.execute(query, parameters)
        cursor.fetchall()

        end = time.perf_counter()

        times.append((end - start) * 1000)

    connection.close()

    average_ms = sum(times) / len(times)

    print(
        f"{name:<25}: "
        f"{average_ms:.3f} ms"
    )

    return average_ms

def run_benchmark(record_count):
    print()
    print("=" * 60)
    print(f"REKORDOK SZÁMA: {record_count}")
    print("=" * 60)

    # Index nélküli adatbázis
    create_database(DATABASE_NO_INDEX)
    insert_test_data(
        DATABASE_NO_INDEX,
        record_count
    )

    # Indexelt adatbázis
    create_database(DATABASE_INDEXED)
    insert_test_data(
        DATABASE_INDEXED,
        record_count
    )
    create_indexes(DATABASE_INDEXED)

    print()
    print("--- INDEX NÉLKÜL ---")
    without_indexes = measure_all(
        DATABASE_NO_INDEX
    )

    print()
    print("--- INDEXEKKEL ---")
    with_indexes = measure_all(
        DATABASE_INDEXED
    )

    print()
    print("--- VÁLTOZÁS ---")

    for name in without_indexes:
        old = without_indexes[name]
        new = with_indexes[name]

        improvement = (
            ((old - new) / old) * 100
            if old > 0
            else 0
        )

        print(
            f"{name:<25}: "
            f"{old:.3f} ms -> "
            f"{new:.3f} ms "
            f"({improvement:+.2f}%)"
        )

if __name__ == "__main__":
    for size in [
        100,
        1000,
        10000
    ]:
        run_benchmark(size)

    for database_path in [
        DATABASE_NO_INDEX,
        DATABASE_INDEXED
    ]:
        if database_path.exists():
            os.remove(database_path)