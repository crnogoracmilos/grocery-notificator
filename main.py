import time
from crawler.maxi_crawler import get_category_urls
from scraper.maxi_scraper import parsing, find_the_prices
from data.sqllite import insert

CATEGORIES = [
    "https://cenoteka.rs/jaja/",
    "https://cenoteka.rs/mleko/",
    "https://cenoteka.rs/ulje/",
]

def main():
    all_products_urls = set()

    for category_url in CATEGORIES:
        urls = get_category_urls(category_url)
        print(f"For {category_url} the software found {len(urls)} products")
        all_products_urls.update(urls)
    print(f"There is {len(all_products_urls)} to scrape")

    for i, url in enumerate(all_products_urls, 1):
        print(f"[{i}/{len(all_products_urls)}] {url}")
        html = parsing(url)
        result = find_the_prices(html)

        if result:
          print(f"Pronađeno cena za {url}: {result}")
          for best_store, best_price, best_name, best_category in result:
            insert(best_name, best_store, best_category, best_price, url, True)
        else:
          print(f"  Skipped (no price found): {url}")
        time.sleep(1)  # be polite to the server

if __name__ == "__main__":
    main()