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


def find_products(search_term: str, limit: int = 5):
    search_term = search_term.strip()

    if not search_term:
        return []

    search_words = search_term.split()
    conditions = " AND ".join(
        ["p.grocery LIKE ?" for _ in search_words]
    )

    parameters = [
        f"%{word}%" for word in search_words
    ]

    parameters.append(limit)

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        sql_find_products = (
        f"""
            SELECT p.grocery, p.store, p.category, ph.price, p.url
            FROM products AS p
            JOIN price_history AS ph
                ON ph.product_id = p.id
            WHERE {conditions} AND ph.id = (
                                            SELECT ph_latest.id
                                            FROM price_history AS ph_latest
                                            WHERE ph_latest.product_id = p.id
                                            ORDER BY ph_latest.timestamp DESC, ph_latest.id DESC
                                            LIMIT 1
                                            )
            AND ph.in_stock = 1
            ORDER BY ph.price ASC
            LIMIT ?
            """
        )
        cursor.execute(sql_find_products, parameters)


        return cursor.fetchall()

if __name__ == "__main__":
    results = find_products("jaja 10kom", 5)

    for product in results:
        print(product)

