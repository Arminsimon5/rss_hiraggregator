from categorizer import categorize_article


def test_electric_car():
    result = categorize_article(
        "Új elektromos autót mutattak be",
        "Az akkumulátor nagyobb hatótávot biztosít."
    )

    assert result == "Elektromos autók"


def test_motorsport():
    result = categorize_article(
        "F1: új szabályok jönnek a következő nagydíjon",
        "A Formula 1 mezőnye készül a versenyre."
    )

    assert result == "Motorsport"


def test_car_test():
    result = categorize_article(
        "Teszteltük az új Mazda MX-5-öt",
        "Menetpróba közúton és autópályán."
    )

    assert result == "Autótesztek"


def test_new_car():
    result = categorize_article(
        "Bemutatták az új Toyota modellt",
        "Az új modell jövőre érkezik Európába."
    )

    assert result == "Új autók"


def test_tuning():
    result = categorize_article(
        "Tuningcsomagot kapott a BMW",
        "A teljesítménynövelés után több lóerő áll rendelkezésre."
    )

    assert result == "Tuning"


def test_traffic():
    result = categorize_article(
        "Baleset történt az autópályán",
        "Útlezárás és jelentős forgalom alakult ki."
    )

    assert result == "Közlekedés"


def test_other():
    result = categorize_article(
        "Egy különleges veterán autó története",
        "A jármű több évtizede ugyanannál a tulajdonosnál van."
    )

    assert result == "Egyéb"


def test_multiple_categories():
    result = categorize_article(
        "Elektromos BMW-t teszteltünk",
        "Az akkumulátor és a töltés volt a teszt középpontjában."
    )

    assert result == "Elektromos autók"