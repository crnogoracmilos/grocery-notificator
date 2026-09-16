import sqlite3

import pytest

import data.sqllite as database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    temporary_db = tmp_path / "test_groceries.db"

    monkeypatch.setattr(
        database,
        "db_path",
        temporary_db,
    )

    with sqlite3.connect(temporary_db) as connection:
        connection.executescript(database.sql_create_table)

    return temporary_db