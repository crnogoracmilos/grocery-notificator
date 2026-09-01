import re
from bs4 import BeautifulSoup
import requests
import time
from data.sqllite import insert



def parsing(url, timeout = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        # Proverava da li je status kod 2xx (baca HTTPError za 404, 403, 500...)
        response.raise_for_status()

        return response.text

    except requests.exceptions.Timeout:
        print(f"Greška: Isteklo vreme (timeout) prilikom učitavanja stranice: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP greška za {url}: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Došlo je do mrežne greške: {e}")

    return None



def find_the_least_expensive(html_content):
    if not html_content:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
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
                    print(f"No price for {store_name}")
        if not d:
            print("Price finding failed")
            return None
        d_sorted = sorted(d.items(), key=lambda item: item[1][0])
        best_store, (best_price, best_name, best_category) = d_sorted[0]
        print(f"The best store for buying is: {best_store}, with the price being {best_price} (Name: {best_name})")
        return d_sorted[0]
    return None

if "__main__" == __name__:
    url = 'https://cenoteka.rs/p/maslinovo-ulje-olitalia-extra-virgine-1l/'
    soup = parsing(url)
    result = find_the_least_expensive(soup)

    if result:
        best_store, (best_price, best_name, best_category) = result
        insert(best_name, best_store, best_category, best_price, url, True)
    else:
        print("Insertion of the data FAILED")