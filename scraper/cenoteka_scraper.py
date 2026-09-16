import re
from bs4 import BeautifulSoup
import requests

def parsing(url, timeout = 10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)

        response.raise_for_status()

        return response.text

    except requests.exceptions.Timeout:
        print(f"Greška: Isteklo vreme (timeout) prilikom učitavanja stranice: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP greška za {url}: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Došlo je do mrežne greške: {e}")

    return None

def parse_price(price_text):
    if not price_text:
        return None
    match = re.search( r'(?<!\d)(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d{2}))?(?!\d)',
        price_text,)

    if not match:
        return None

    whole_part = match.group(1).replace('.', '')
    decimal_part = match.group(2) or '00'

    return float(f"{whole_part}.{decimal_part}")

def find_the_prices(html_content):
    if not html_content:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')

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

    prices_html = soup.find_all('div', class_=re.compile(r'priceCol'))
    if not prices_html:
        prices_html = [soup]
    units = []
    for col in prices_html:
        row = col.find_all(['div', 'a'], class_=re.compile(r'__row'))

        for prices_row in row:
            store = prices_row.find('img', class_=re.compile(r'logo'))
            store_name = store.get('alt','unknown') if store else 'unknown'
            price_span = prices_row.find('span', class_=re.compile(r'price'))
            if not price_span:
                continue
            price_text = price_span.get_text(strip=True)
            price = parse_price(price_text)

            if price is None:
                print(f"No valid price for {store_name}: {price_text}")
                continue
            units.append((
                store_name,
                price,
                name,
                category,
            ))
    if not units:
        print("Price finding failed")
        return None
    return units


