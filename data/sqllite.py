import sqlite3
from pathlib import Path
from core.text import normalize_search
from contextlib import closing

#the database file tends to appear in scraper folder
data_folder = Path(__file__).parent.absolute()
db_path = data_folder / 'groceries.db'

#creating a table
sql_create_table = """
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grocery TEXT NOT NULL,
    grocery_search TEXT NOT NULL,
    store TEXT NOT NULL,
    store_search TEXT NOT NULL,
    category TEXT,
    url TEXT NOT NULL,
    UNIQUE(url, store_search)
);
CREATE TABLE IF NOT EXISTS price_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price REAL,
    in_stock BOOLEAN,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY(product_id) REFERENCES products(id)
);
CREATE INDEX IF NOT EXISTS idx_price_history_product_latest
    ON price_history (
        product_id,
        timestamp DESC,
        id DESC
);
"""


def initial_database():
    with closing(sqlite3.connect(db_path)) as connection:
        connection.executescript(sql_create_table)


def insert(grocery, store, category, price, url, in_stock):
    grocery_search = normalize_search(grocery)
    store_search = normalize_search(store)
    try:
        with closing(sqlite3.connect(db_path)) as connection:
            with connection:
                cursor = connection.cursor()
                sql_insert_product = """
                INSERT INTO products (grocery, grocery_search, store, store_search, category, url)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(url, store_search)
                DO UPDATE SET
                grocery = CASE
                    WHEN excluded.grocery_search NOT IN ('', 'unknown')
                    THEN excluded.grocery
                    ELSE products.grocery
                    END,

                grocery_search = CASE
                    WHEN excluded.grocery_search NOT IN ('', 'unknown')
                    THEN excluded.grocery_search
                    ELSE products.grocery_search
                END,

                category = CASE
                    WHEN excluded.category IS NOT NULL
                     AND lower(trim(excluded.category)) NOT IN ('', 'unknown')
                    THEN excluded.category
                    ELSE products.category
                END;
            """
                cursor.execute(sql_insert_product, (grocery, grocery_search, store, store_search, category, url))
                sql_get_id = """
                                SELECT id FROM products 
                                WHERE url = ? AND store_search = ?;
                            """
                cursor.execute(sql_get_id,(url, store_search))
                result = cursor.fetchone()
                if result is None:
                    raise Exception("The ID was not found during the search")
                product_id = result[0]
                sql_insert_price = """
                            INSERT INTO price_history (product_id, price, in_stock)
                            VALUES (?, ?, ?);
                        """
                cursor.execute(sql_insert_price, (product_id, price, in_stock))
    except Exception as e:
        print(f"Error at update {e}")
        raise

def escape_like(text: str) -> str:
    return (
        text
        .replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def find_products(search_term: str, limit: int = 5):
    search_term = normalize_search(search_term)

    if not search_term:
        return []

    search_words = search_term.split()
    conditions = " AND ".join(
        ["p.grocery_search LIKE ? ESCAPE '\\'" for _ in search_words]
    )

    parameters = [
        f"%{escape_like(word)}%" for word in search_words
    ]

    parameters.append(limit)

    with closing(sqlite3.connect(db_path)) as connection:
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
    initial_database()
    results = find_products("jaja 10kom", 5)

    for product in results:
        print(product)

