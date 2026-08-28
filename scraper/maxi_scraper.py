import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome()
url = 'https://cenoteka.rs/p/jaja-klasa-m-10kom/'

try:
    driver.get(url)
    time.sleep(3)
    html_code = driver.page_source
finally:
    driver.quit()

soup = BeautifulSoup(html_code, features='html.parser')
prices_html = soup.find('div', class_=re.compile(r'priceCol'))
if prices_html:
    row = prices_html.find_all('div', class_=re.compile(r'row'))
    d = dict()
    for prices in row:
        store = prices.find('img', class_=re.compile(r'logo'))
        store_name = store['alt'] if store else 'unknown'

        price_span = prices.find('span', class_=re.compile(r'price'))
        price_text = price_span.text.strip() if price_span else 'unknown'

        if price_span and price_span.text.strip():
            price_text = price_span.text.strip()
            price = float(price_text.replace(',', '.'))
            d[store_name] = price
    if d:
        min_price = min(d.values())
        best_store = " ".join([store for store, price in d.items() if price == min_price])
        print(best_store)
else:
    print("The program was unable to find the prices")


