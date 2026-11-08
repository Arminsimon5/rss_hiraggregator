import re


EXACT_KEYWORDS = {
    "teszt",
    "ev",
    "f1",
    "út"
}


def contains_keyword(text, keyword):
    if keyword in EXACT_KEYWORDS:
        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
        return re.search(
            pattern,
            text,
            re.IGNORECASE
        ) is not None

    return keyword.lower() in text.lower()

def categorize_article(title, summary):
    title_text = title.lower()
    summary_text = summary.lower()

    categories = {
        "Elektromos autók": {
            "elektromos": 2,
            "villanyautó": 4,
            "elektromobilitás": 4,
            "akkumulátor": 3,
            "töltés": 3,
            "töltő": 3,
            "tölthet": 3,
            "hatótáv": 3,
            "konnektoros": 5,
            "plug-in": 4,
            "phev": 4,
            "tesla": 2,
            "zéró emisszió": 4,
            "belsőégésű-tilalom": 5
        },

        "Motorsport": {
            "forma-1": 6,
            "formula 1": 6,
            "f1": 6,
            "motogp": 6,
            "wrc": 6,
            "rali": 5,
            "rally": 5,
            "motorsport": 5,
            "nagydíj": 5,
            "futam": 5,
            "időmérő": 5,
            "rajtrács": 4,
            "pole": 4,
            "pilóta": 4,
            "versenyző": 4,
            "csapattárs": 3,
            "világbajnok": 3
        },

        "Autótesztek": {
            "teszt": 3,
            "menetpróba": 3,
            "kipróbáltuk": 3,
            "vezettük": 3,
            "próba": 1
        },

        "Új autók": {
            "bemutatták": 8,
            "bemutatkozott": 8,
            "új modell": 7,
            "új generáció": 8,
            "vadonatúj": 7,
            "premier": 6,
            "világpremier": 8,
            "leplezték le": 8,
            "leleplezték": 8,
            "debütált": 8,
            "modellfrissítés": 6,
            "frissített modell": 6,
            "megérkezett": 5,
            "érkezik": 4,
            "rendelhető": 3,
            "piacra kerül": 5
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
            "baleset": 6,
            "karambol": 6,
            "ütközés": 5,
            "forgalom": 4,
            "forgalmi": 3,
            "autópálya": 3,
            "útlezárás": 6,
            "lezárták": 5,
            "lezárás": 5,
            "torlódás": 6,
            "dugó": 5,
            "traffipax": 6,
            "kresz": 6,
            "rendőrség": 3,
            "rendőr": 3,
            "gyorshajtás": 5,
            "sebességhatár": 5,
            "közlekedés": 4,
            "közlekedési": 4,
            "jogosítvány": 4,
            "bírság": 4,
            "büntetés": 3,
            "parkolás": 4,
            "útépítés": 4,
            "üzemanyagár": 6,
            "üzemanyag ára": 6,
            "üzemanyagok ára": 6,
            "nagykereskedelmi ár": 5,
            "benzin ára": 5,
            "gázolaj ára": 5
        }
    }

    scores = {
        category: 0
        for category in categories
    }
    
    for category, keywords in categories.items():
        for keyword, points in keywords.items():

            if contains_keyword(title_text, keyword):
                scores[category] += points * 2

            if contains_keyword(summary_text, keyword):
                scores[category] += points


    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return "Egyéb"

    return best_category