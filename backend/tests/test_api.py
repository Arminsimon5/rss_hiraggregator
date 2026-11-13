from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import database
from api import app


TEST_DATABASE_PATH = Path(__file__).resolve().parent / "test_news.db"

client = TestClient(app)


@pytest.fixture(autouse=True)
def test_database():
    database.DATABASE_PATH = TEST_DATABASE_PATH

    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()

    database.create_database()

    test_articles = [
        {
            "title": "Új Mazda MX-5 mutatkozott be",
            "link": "https://example.com/mazda-mx5",
            "published": "2026-11-12T12:00:00+00:00",
            "summary": "A Mazda bemutatta legújabb modelljét.",
            "source": "Vezess",
            "category": "Új autók"
        },
        {
            "title": "Forma-1 futam eredmények",
            "link": "https://example.com/f1",
            "published": "2026-11-11T12:00:00+00:00",
            "summary": "A hétvégi Forma-1-es futam összefoglalója.",
            "source": "Racingline",
            "category": "Motorsport"
        },
        {
            "title": "Elektromos autók hatótávja",
            "link": "https://example.com/electric",
            "published": "2026-11-10T12:00:00+00:00",
            "summary": "Új elektromos modellek hatótávját vizsgálták.",
            "source": "Villanyautosok",
            "category": "Elektromos autók"
        },
        {
            "title": "Üzemanyagár-változás",
            "link": "https://example.com/fuel",
            "published": "2026-10-01T12:00:00+00:00",
            "summary": "Változnak a hazai üzemanyagárak.",
            "source": "Autonavigator",
            "category": "Közlekedés"
        }
    ]

    for article in test_articles:
        database.save_article(article)

    yield

    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()


def test_articles_endpoint():
    response = client.get("/articles")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

    assert data["total"] == 4
    assert len(data["items"]) == 4


def test_articles_pagination():
    response = client.get("/articles?limit=2&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert data["limit"] == 2
    assert data["offset"] == 0
    assert len(data["items"]) == 2
    assert data["total"] == 4


def test_articles_category_filter():
    response = client.get(
        "/articles?category=Motorsport"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["category"] == "Motorsport"


def test_articles_source_filter():
    response = client.get(
        "/articles?source=Vezess"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["source"] == "Vezess"


def test_articles_search():
    response = client.get(
        "/articles?search=Mazda"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1

    article = data["items"][0]

    assert "mazda" in (
        article["title"] + " " + article["summary"]
    ).lower()


def test_articles_period_filter():
    response = client.get(
        "/articles?period=week"
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "total" in data