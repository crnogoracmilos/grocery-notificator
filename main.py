import time
from crawler.cenoteka_crawler import get_category_urls
from scraper.cenoteka_scraper import parsing, find_the_prices
from data.sqllite import insert
from processors.process import find_the_categories



def main():
    print("The bot has been activated and is reading the messages...")
    """while True:
        text = handle_response()
        if not text:
            time.sleep(2)
            continue
        print(f"The message has been received: {text}")"""
    category_url = find_the_categories('brasno')
    all_products_urls = set()
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
    print("This message has been done with, waiting for the next one...")

if __name__ == "__main__":
    main()