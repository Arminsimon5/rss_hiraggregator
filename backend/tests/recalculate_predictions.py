import csv

from categorizer import categorize_article


INPUT_FILE = "evaluation_sample_filled.csv"
OUTPUT_FILE = "evaluation_sample_v3.csv"


def recalculate_predictions():
    rows = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        fieldnames = reader.fieldnames

        for row in reader:
            title = row["title"]
            summary = row["summary"]

            row["predicted_category"] = categorize_article(
                title or "",
                summary or ""
            )

            rows.append(row)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"{len(rows)} hír újrakategorizálva: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    recalculate_predictions()