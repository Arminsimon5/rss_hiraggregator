import csv
from collections import defaultdict


INPUT_FILE = "evaluation_sample_filled.csv"


def evaluate():
    total = 0
    correct = 0

    category_total = defaultdict(int)
    category_correct = defaultdict(int)

    confusion = defaultdict(lambda: defaultdict(int))

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            predicted = row["predicted_category"].strip()
            manual = row["manual_category"].strip()

            if not manual:
                continue

            total += 1
            category_total[manual] += 1

            confusion[manual][predicted] += 1

            if predicted == manual:
                correct += 1
                category_correct[manual] += 1

    if total == 0:
        print("Nincs kiértékelhető adat.")
        return

    accuracy = correct / total * 100

    print()
    print("=== ÖSSZESÍTÉS ===")
    print(f"Vizsgált hírek: {total}")
    print(f"Helyes besorolások: {correct}")
    print(f"Hibás besorolások: {total - correct}")
    print(f"Pontosság: {accuracy:.2f}%")

    print()
    print("=== KATEGÓRIÁNKÉNT ===")

    for category in sorted(category_total):
        count = category_total[category]
        correct_count = category_correct[category]

        category_accuracy = (
            correct_count / count * 100
            if count > 0
            else 0
        )

        print(
            f"{category}: "
            f"{correct_count}/{count} "
            f"({category_accuracy:.2f}%)"
        )

    print()
    print("=== TÉVES BESOROLÁSOK ===")

    for manual_category in sorted(confusion):
        print()
        print(f"Valódi kategória: {manual_category}")

        for predicted_category, count in sorted(
            confusion[manual_category].items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(
                f"  -> {predicted_category}: {count}"
            )


if __name__ == "__main__":
    evaluate()