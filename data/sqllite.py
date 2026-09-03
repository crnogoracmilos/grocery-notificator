import sqlite3
from pathlib import Path

#the database file tends to appear in scraper folder
data_folder = Path(__file__).parent.absolute()
db_path = data_folder / 'groceries.db'

#creating a table
sql_create_table = """
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grocery TEXT NOT NULL,
    store TEXT,
    category TEXT,
    url TEXT,
    UNIQUE(url, store)
);
CREATE TABLE IF NOT EXISTS price_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price REAL,
    in_stock BOOLEAN,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(product_id) REFERENCES products(id)
);

"""
with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()
    cursor.executescript(sql_create_table)
    connection.commit()

def insert(grocery, store, category, price, url, in_stock):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            sql_insert_product = """
                INSERT OR IGNORE INTO products (grocery, store, category, url)
                VALUES (?, ?, ?, ?);
                """
            cursor.execute(sql_insert_product, (grocery, store, category, url))
            sql_get_id = """
                            SELECT id FROM products 
                            WHERE url = ? AND store = ?;
                        """
            cursor.execute(sql_get_id,(url, store))
            result = cursor.fetchone()
            if result is None:
                raise Exception("The ID was not found during the search")
            product_id = result[0]
            sql_insert_price = """
                            INSERT INTO price_history (product_id, price, in_stock)
                            VALUES (?, ?, ?);
                        """
            cursor.execute(sql_insert_price, (product_id, price, in_stock))
            connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error at update {e}")


