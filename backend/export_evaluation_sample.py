import csv
import random

from database import get_connection
from categorizer import categorize_article


SAMPLE_SIZE = 100
OUTPUT_FILE = "evaluation_sample.csv"


def export_sample():
    connection = get_connection()
    connection.row_factory = None

    cursor = connection.cursor()

    cursor.execute("""
        SELECT title, summary
        FROM articles
        WHERE title IS NOT NULL
        ORDER BY id DESC
        LIMIT 500
    """)

    articles = cursor.fetchall()
    connection.close()

    if len(articles) > SAMPLE_SIZE:
        articles = random.sample(articles, SAMPLE_SIZE)

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "title",
            "summary",
            "predicted_category",
            "manual_category"
        ])

        for title, summary in articles:
            predicted_category = categorize_article(
                title or "",
                summary or ""
            )

            writer.writerow([
                title,
                summary,
                predicted_category,
                ""
            ])

    print(
        f"{len(articles)} hír exportálva: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    export_sample()