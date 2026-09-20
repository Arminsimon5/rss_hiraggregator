def categorize_article(title, summary):
    text = (title + " " + summary).lower()

    categories = {
        "Elektromos autók": [
            "elektromos",
            "villanyautó",
            "akkumulátor",
            "töltés",
            "tesla",
            "ev"
        ],

        "Motorsport": [
            "forma-1",
            "formula 1",
            "f1",
            "rali",
            "rally",
            "wrc",
            "motorsport"
        ],

        "Autótesztek": [
            "teszt",
            "menetpróba",
            "kipróbáltuk",
            "vezettük"
        ],

        "Új autók": [
            "bemutatták",
            "új modell",
            "premier",
            "bemutatkozott",
            "érkezik"
        ],

        "Tuning": [
            "tuning",
            "tuner",
            "átalakítás",
            "lóerő",
            "teljesítménynövelés"
        ],

        "Közlekedés": [
            "baleset",
            "forgalom",
            "autópálya",
            "útlezárás",
            "traffipax",
            "kresz"
        ]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Egyéb"