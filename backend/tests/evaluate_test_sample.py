import csv
from pathlib import Path
from collections import defaultdict

from categorizer import categorize_article


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "test_sample_filled.csv"


def evaluate():
    total = 0
    correct = 0

    category_total = defaultdict(int)
    category_correct = defaultdict(int)

    true_positive = defaultdict(int)
    false_positive = defaultdict(int)
    false_negative = defaultdict(int)

    confusion = defaultdict(lambda: defaultdict(int))

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            title = row["title"].strip()
            summary = row["summary"].strip()
            manual = row["manual_category"].strip()

            if not manual:
                continue

            predicted = categorize_article(
                title,
                summary
            )

            total += 1
            category_total[manual] += 1

            confusion[manual][predicted] += 1

            if predicted == manual:
                correct += 1
                category_correct[manual] += 1
                true_positive[manual] += 1

            else:
                false_positive[predicted] += 1
                false_negative[manual] += 1

    if total == 0:
        print("Nincs kiértékelhető adat.")
        return

    accuracy = correct / total * 100

    print()
    print("=== FÜGGETLEN TESZT ===")
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
    print("=== PRECISION / RECALL / F1 ===")

    all_categories = sorted(category_total.keys())

    f1_scores = []

    for category in all_categories:
        tp = true_positive[category]
        fp = false_positive[category]
        fn = false_negative[category]

        precision = (
            tp / (tp + fp)
            if (tp + fp) > 0
            else 0
        )

        recall = (
            tp / (tp + fn)
            if (tp + fn) > 0
            else 0
        )

        f1 = (
            2 * precision * recall
            / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        f1_scores.append(f1)

        print(
            f"{category}: "
            f"Precision={precision:.2%}, "
            f"Recall={recall:.2%}, "
            f"F1={f1:.2%}"
        )

    macro_f1 = (
        sum(f1_scores) / len(f1_scores)
        if f1_scores
        else 0
    )

    print()
    print(f"Macro F1: {macro_f1:.2%}")

    print()
    print("=== TÉVES BESOROLÁSOK ===")

    for manual_category in sorted(confusion):
        print()
        print(
            f"Valódi kategória: "
            f"{manual_category}"
        )

        for predicted_category, count in sorted(
            confusion[manual_category].items(),
            key=lambda item: item[1],
            reverse=True
        ):
            print(
                f"  -> {predicted_category}: "
                f"{count}"
            )

    
    print()
    print("=== CONFUSION MATRIX ===")
    
    categories = sorted(category_total.keys())
    
    print(f"{'Valódi / Jósolt':<22}", end="")
    
    for category in categories:
        print(f"{category[:10]:>12}", end="")
    
    print()
    
    for manual_category in categories:
        print(f"{manual_category:<22}", end="")
    
        for predicted_category in categories:
            value = confusion[manual_category][predicted_category]
            print(f"{value:>12}", end="")
    
        print()


if __name__ == "__main__":
    evaluate()