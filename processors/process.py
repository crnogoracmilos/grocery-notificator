import pandas as pd
import sqlite3
from pathlib import Path

current_file = Path(__file__).resolve()

db_path = current_file.parent.parent / 'data' / 'groceries.db'

with sqlite3.connect(db_path) as connection:
    data = pd.read_sql("SELECT * FROM groceries", connection)

lowest_price = data.loc[data.groupby('grocery')['price'].idxmin()]
average_price = data.loc[data.groupby('category')['price'].idxmin()]
print(lowest_price[['grocery', 'store', 'price']])
print(average_price[['grocery', 'store', 'price']])
