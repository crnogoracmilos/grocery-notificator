import pandas as pd
import sqlite3
from pathlib import Path

current_file = Path(__file__).resolve()

db_path = current_file.parent.parent / 'data' / 'groceries.db'

with sqlite3.connect(db_path) as connection:
    data = pd.read_sql("SELECT * FROM price_history", connection)

def find_lowest():
    lowest_price = data.loc[data.groupby('grocery')['price'].idxmin()]
    return lowest_price[['grocery', 'store', 'price', 'url']]

def find_the_categories(text):
    text_parsed = text.replace(' ','%20').lower()
    link = f"https://cenoteka.rs/pretraga/?q={text_parsed}"
    return link
