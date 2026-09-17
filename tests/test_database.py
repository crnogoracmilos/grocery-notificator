import sqlite3

import pytest

import data.sqllite as database


def test_database_starts_empty(test_db):
    with sqlite3.connect(test_db) as connection:
        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        price_count = connection.execute(
            "SELECT COUNT(*) FROM price_history"
        ).fetchone()[0]

    assert product_count == 0
    assert price_count == 0


def test_insert_saves_product_and_price(test_db):
    database.insert(
        grocery="Čokoladno mleko 1l",
        store="Maxi",
        category="Mleko",
        price=149.99,
        url="https://example.test/cokoladno-mleko",
        in_stock=True,
    )

    with sqlite3.connect(test_db) as connection:
        product = connection.execute(
            """
            SELECT grocery, store, category, url
            FROM products
            """
        ).fetchone()

        price = connection.execute(
            """
            SELECT price, in_stock
            FROM price_history
            """
        ).fetchone()

    assert product == (
        "Čokoladno mleko 1l",
        "Maxi",
        "Mleko",
        "https://example.test/cokoladno-mleko",
    )

    assert price[0] == pytest.approx(149.99)
    assert price[1] == 1

def test_search_is_case_insensitive_for_serbian_letters(test_db):
        database.insert(
            grocery="Čokoladna jaja",
            store="Maxi",
            category="Slatkiši",
            price=299.99,
            url="https://example.test/cokoladna-jaja",
            in_stock=True,
        )

        uppercase_results = database.find_products("Čokoladna")
        lowercase_results = database.find_products("čokoladna")

        assert uppercase_results == lowercase_results
        assert len(lowercase_results) == 1


def test_store_case_does_not_create_duplicate(test_db):
    database.insert(
        "Mleko",
        "Maxi",
        "Mleko",
        100,
        "https://example.test/mleko",
        True,
    )

    database.insert(
        "Mleko",
        "maxi",
        "Mleko",
        110,
        "https://example.test/mleko",
        True,
    )

    with sqlite3.connect(test_db) as connection:
        product_count = connection.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        price_count = connection.execute(
            "SELECT COUNT(*) FROM price_history"
        ).fetchone()[0]

    assert product_count == 1
    assert price_count == 2