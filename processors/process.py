import pandas as pd
import sqlite3
from pathlib import Path
from urllib.parse import urlencode
from core.text import normalize_search
from contextlib import closing

current_file = Path(__file__).resolve()

db_path = current_file.parent.parent / 'data' / 'groceries.db'



def find_lowest():
    with closing(sqlite3.connect(db_path)) as connection:
        data = pd.read_sql(''' SELECT
                                p.grocery,
                               p.store,
                               p.url,
                               ph.price,
                               ph.in_stock,
                               ph.timestamp
                               FROM products p
                               JOIN price_history ph
                               ON p.id = ph.product_id
                               WHERE ph.id=(
                                SELECT ph_latest.id
                                FROM price_history AS ph_latest
                                WHERE ph_latest.product_id = p.id
                                ORDER BY
                                    ph_latest.timestamp DESC,
                                    ph_latest.id DESC
                                LIMIT 1                             
                                ) AND ph.in_stock=1''', connection)
        connection.execute()
    lowest_price = data.loc[data.groupby('grocery')['price'].idxmin()]
    return lowest_price[['grocery', 'store', 'price', 'url']]

def find_the_categories(text: str) -> str:
    query = urlencode({"q": normalize_search(text)})
    return f"https://cenoteka.rs/pretraga/?{query}"


if "__main__" == __name__:
    find_lowest()