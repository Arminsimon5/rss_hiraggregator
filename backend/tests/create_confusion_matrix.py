import csv
from pathlib import Path

import matplotlib.pyplot as plt

from categorizer import categorize_article


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "test_sample_filled.csv"
OUTPUT_FILE = BASE_DIR / "confusion_matrix.png"


CATEGORIES = [
    "Autótesztek",
    "Egyéb",
    "Elektromos autók",
    "Közlekedés",
    "Motorsport",
    "Tuning",
    "Új autók"
]


def create_confusion_matrix():
    matrix = [
        [0 for _ in CATEGORIES]
        for _ in CATEGORIES
    ]

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            manual = row["manual_category"].strip()

            if not manual:
                continue

            predicted = categorize_article(
                row["title"].strip(),
                row["summary"].strip()
            )

            if manual not in CATEGORIES:
                continue

            if predicted not in CATEGORIES:
                continue

            actual_index = CATEGORIES.index(manual)
            predicted_index = CATEGORIES.index(predicted)

            matrix[actual_index][predicted_index] += 1

    fig, ax = plt.subplots(figsize=(10, 8))

    image = ax.imshow(matrix)

    ax.set_xticks(range(len(CATEGORIES)))
    ax.set_yticks(range(len(CATEGORIES)))

    ax.set_xticklabels(
        CATEGORIES,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(CATEGORIES)

    ax.set_xlabel("Jósolt kategória")
    ax.set_ylabel("Valódi kategória")

    ax.set_title(
        "Kategorizáló algoritmus – Confusion Matrix"
    )

    for i in range(len(CATEGORIES)):
        for j in range(len(CATEGORIES)):
            ax.text(
                j,
                i,
                matrix[i][j],
                ha="center",
                va="center"
            )

    fig.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Confusion matrix elkészült: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    create_confusion_matrix()