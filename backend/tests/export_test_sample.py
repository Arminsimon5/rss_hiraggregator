import csv
import random

from database import get_connection


DEVELOPMENT_FILE = "evaluation_sample_filled.csv"
OUTPUT_FILE = "test_sample.csv"

SAMPLE_SIZE = 95
RANDOM_SEED = 42


def load_development_titles():
    titles = set()

    with open(
        DEVELOPMENT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            title = row["title"].strip()

            if title:
                titles.add(title)

    return titles


def export_test_sample():
    development_titles = load_development_titles()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, summary
        FROM articles
        WHERE title IS NOT NULL
    """)

    articles = cursor.fetchall()
    connection.close()

    available_articles = []

    for title, summary in articles:
        if title not in development_titles:
            available_articles.append(
                (
                    title,
                    summary or ""
                )
            )

    print(
        f"Első mintában szereplő hírek: "
        f"{len(development_titles)}"
    )

    print(
        f"Független mintához elérhető hírek: "
        f"{len(available_articles)}"
    )

    if len(available_articles) < SAMPLE_SIZE:
        print(
            "Nincs még elegendő új hír "
            "100 elemű független mintához."
        )
        return

    random.seed(RANDOM_SEED)

    sample = random.sample(
        available_articles,
        SAMPLE_SIZE
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "title",
            "summary",
            "manual_category"
        ])

        for title, summary in sample:
            writer.writerow([
                title,
                summary,
                ""
            ])

    print()
    print(
        f"{len(sample)} független hír exportálva: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    export_test_sample()