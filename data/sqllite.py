import sqlite3
import pandas as pd
from pathlib import Path

#the database file tends to appear in scraper folder
data_folder = Path(__file__).parent.absolute()
db_path = data_folder / 'groceries.db'

#connection
connection = sqlite3.connect(db_path)

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
cursor = connection.cursor()
cursor.execute(sql_create_table)
try:
    connection.commit()
except Exception as e:
    connection.rollback()

def insert(grocery, store, category, price, url, in_stock):
    sql_insert = """
    INSERT INTO groceries (grocery, store, category, price, url, in_stock) 
    VALUES (?,?,?,?,?,?)
    ON CONFLICT(url) DO UPDATE SET
        price = excluded.price,
        in_stock = excluded.in_stock;
    """
    try:
        cursor.execute(sql_insert, (grocery, store, category, price, url, in_stock))
        connection.commit()
        print(f"Item: {grocery} successfully updated")
    except Exception as e:
        connection.rollback()
        print("Error at update")


