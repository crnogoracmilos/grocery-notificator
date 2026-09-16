import re
import time
from http.client import responses

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def get_category_urls(category_url):
    product_urls = set()
    visited_pages = set()
    current_url = category_url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    while current_url and current_url not in visited_pages:
        visited_pages.add(current_url)
        try:
            response = requests.get(current_url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error at {current_url}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        excluded = set()
        widget_heading = soup.find(string=re.compile('trenutno najtraženije', re.I))
        if widget_heading:
            widget_section = widget_heading.find_parent(['div', 'section', 'nav', 'aside'])
            if widget_section:
                for a in widget_section.find_all('a', href = True):
                    excluded.add(urljoin("https://cenoteka.rs", a['href']))

        links = soup.find_all('a', href = re.compile(r'/p/'))
        for link in links:
            full_url = urljoin("https://cenoteka.rs", link['href'])
            if full_url not in excluded:
                product_urls.add(full_url)
        next_button = soup.select_one('nav[aria-label="Paginacija"] a[aria-label="Sledeća strana"]')
        current_url = urljoin("https://cenoteka.rs", next_button['href']) if next_button and next_button.get(
            'href') else None
        time.sleep(0.5)
    return list(product_urls)

if __name__ == "__main__":
    links = get_category_urls("https://cenoteka.rs/pretraga/?q=majmun")
    print(links)
    print(len(links))
