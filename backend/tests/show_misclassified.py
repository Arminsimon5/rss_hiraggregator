import csv


INPUT_FILE = "evaluation_sample_v2.csv"


def show_misclassified():
    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            predicted = row["predicted_category"].strip()
            manual = row["manual_category"].strip()

            if predicted != manual:
                print("=" * 80)
                print(f"Cím: {row['title']}")
                print(f"Valódi: {manual}")
                print(f"Program: {predicted}")
                print()


if __name__ == "__main__":
    show_misclassified()