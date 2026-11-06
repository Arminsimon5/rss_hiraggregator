def categorize_article(title, summary):
    text = f"{title} {summary}".lower()

    categories = {
        "Elektromos autók": {
            "elektromos": 3,
            "villanyautó": 3,
            "akkumulátor": 2,
            "töltés": 2,
            "tesla": 2,
            "ev": 1
        },

        "Motorsport": {
            "forma-1": 3,
            "formula 1": 3,
            "f1": 3,
            "rali": 3,
            "rally": 3,
            "wrc": 3,
            "motorsport": 2,
            "verseny": 1,
            "nagydíj": 2
        },

        "Autótesztek": {
            "teszt": 3,
            "menetpróba": 3,
            "kipróbáltuk": 3,
            "vezettük": 3,
            "próba": 1
        },

        "Új autók": {
            "bemutatták": 3,
            "új modell": 3,
            "premier": 2,
            "bemutatkozott": 3,
            "érkezik": 1,
            "újdonság": 1
        },

        "Tuning": {
            "tuning": 3,
            "tuner": 3,
            "átalakítás": 2,
            "lóerő": 1,
            "teljesítménynövelés": 3,
            "chiptuning": 3
        },

        "Közlekedés": {
            "baleset": 3,
            "forgalom": 2,
            "autópálya": 2,
            "útlezárás": 3,
            "traffipax": 3,
            "kresz": 3,
            "dugó": 2
        }
    }

    scores = {
        category: 0
        for category in categories
    }

    for category, keywords in categories.items():
        for keyword, points in keywords.items():
            if keyword in text:
                scores[category] += points

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return "Egyéb"

    return best_category