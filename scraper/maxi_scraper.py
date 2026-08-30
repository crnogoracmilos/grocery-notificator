import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver





def parsing():
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
    return prices_html

def find_the_least_expensive(prices_html):
    if prices_html:
        row = prices_html.find_all('div', class_=re.compile(r'row'))
        d = dict()
        for prices in row:
            store = prices.find('img', class_=re.compile(r'logo'))
            store_name = store['alt'] if store else 'unknown'

            price_span = prices.find('span', class_=re.compile(r'price'))

            if price_span and price_span.text.strip():
                price_text = price_span.text.strip() if price_span else 'unknown'
                price = float(price_text.replace('.', '').replace(',','.'))
                d[store_name] = price
            if not d:
                print("Pronalazenje cena je neuspesno")
                return None
        d_sorted = sorted(d.items(), key=lambda item: item[1])
        best_store, best_price = d_sorted[0]
        print(f"The best store for buying eggs is: {best_store}, with the price being {best_price}")
        try:
            return d_sorted[0]
        except RuntimeError("Greska, vrednost nije vracena"):
            return None
    else:
        return None

if "__main__" == __name__:
    print(find_the_least_expensive(parsing()))
