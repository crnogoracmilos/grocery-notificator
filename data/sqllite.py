import sqlite3
from pathlib import Path

#the database file tends to appear in scraper folder
data_folder = Path(__file__).parent.absolute()
db_path = data_folder / 'groceries.db'

#creating a table
sql_create_table = """
CREATE TABLE IF NOT EXISTS groceries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grocery TEXT NOT NULL,
    store TEXT,
    category TEXT,
    price REAL,
    url TEXT UNIQUE,
    in_stock BOOLEAN
)
"""
with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()
    cursor.execute(sql_create_table)
    connection.commit()

def insert(grocery, store, category, price, url, in_stock):
    sql_insert = """
    INSERT INTO groceries (grocery, store, category, price, url, in_stock) 
    VALUES (?,?,?,?,?,?)
    ON CONFLICT(url) DO UPDATE SET
        price = excluded.price,
        in_stock = excluded.in_stock;
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_insert, (grocery, store, category, price, url, in_stock))
            connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error at update {e}")


