import re
from bs4 import BeautifulSoup
import requests
from data import sqllite
from data.sqllite import insert



def parsing(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def find_the_least_expensive(soup):
    prices_html = soup.find('div', class_=re.compile(r'priceCol'))

    line = soup.find('ol', class_ = re.compile(r'list'))
    if line:
        name_span = line.find('span', class_=re.compile(r'current'))
        name = name_span.text.strip() if name_span else "unknown"
        links = line.find_all('a')
        if links:
            category = links[-1].text.strip()
        else:
            category = 'unknown'
    else:
        name = 'unknown'
        category = 'unknown'

    if prices_html:
        row = prices_html.find_all('div', class_=re.compile(r'row'))
        d = dict()
        for prices in row:
            store = prices.find('img', class_=re.compile(r'logo'))
            store_name = store['alt'] if store else 'unknown'
            price_span = prices.find('span', class_=re.compile(r'price'))
            if price_span:
                price_text = price_span.text.strip()
                match = re.search(r'[\d.,]+', price_text)

                if match:
                    clean_price = match.group(0)
                    price = float(clean_price.replace('.', '').replace(',', '.'))
                    d[store_name] = (price, name, category)
                else:
                    print(f"Nije pronađena validna cena za {store_name}")
        if not d:
            print("Pronalazenje cena je neuspesno")
            return None
        d_sorted = sorted(d.items(), key=lambda item: item[1][0])
        best_store, (best_price, best_name, best_category) = d_sorted[0]
        print(f"The best store for buying is: {best_store}, with the price being {best_price} (Name: {best_name})")
        return d_sorted[0]
    return None

if "__main__" == __name__:
    url = 'https://cenoteka.rs/p/krem-ferrero-nutella-400g/'
    soup = parsing(url)
    result = find_the_least_expensive(soup)

    if result:
        best_store, (best_price, best_name, best_category) = result
        insert(best_name, best_store, best_category, best_price, url, True)
    else:
        print("Insertion of the data FAILED")