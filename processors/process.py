import pandas as pd
import sqlite3
from pathlib import Path
import unicodedata
from urllib.parse import urlencode

current_file = Path(__file__).resolve()

db_path = current_file.parent.parent / 'data' / 'groceries.db'

with sqlite3.connect(db_path) as connection:
    data = pd.read_sql("SELECT * FROM price_history", connection)

def normalize_search(text: str) -> str:
    return unicodedata.normalize("NFC", text).strip().casefold()

def find_lowest():
    lowest_price = data.loc[data.groupby('grocery')['price'].idxmin()]
    return lowest_price[['grocery', 'store', 'price', 'url']]

def find_the_categories(text: str) -> str:
    query = urlencode({"q": normalize_search(text)})
    return f"https://cenoteka.rs/pretraga/?{query}"
