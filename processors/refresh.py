import time

from crawler.cenoteka_crawler import get_category_urls
from data.sqllite import insert
from processors.process import find_the_categories
from scraper.cenoteka_scraper import find_the_prices, item_getter

def refresh_prices(query: str) -> None:
    search_url = find_the_categories(query)
    product_urls = get_category_urls(search_url)

    for url in product_urls:
        html = item_getter(url)
        offers = find_the_prices(url)

        if offers is None:
            print(f"Neuspesno citanje ponude za {url}")
        else:
            for store, price, name, category in offers:
                insert(name, store, category, price, url, True)
        time.sleep(1)