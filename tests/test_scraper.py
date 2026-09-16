import pytest

from scraper.cenoteka_scraper import find_the_prices


def make_product_html(*rows: str) -> str:
    joined_rows = "\n".join(rows)

    return f"""
    <html>
        <body>
            <ol class="breadcrumb-list">
                <li><a href="/kategorija/slatkisi">Slatkiši</a></li>
                <li>
                    <span class="breadcrumb-current">
                        Čokolada TEST 100g
                    </span>
                </li>
            </ol>

            <div class="product-priceCol">
                {joined_rows}
            </div>
        </body>
    </html>
    """


def make_price_row(store: str, price: str) -> str:
    return f"""
    <div class="store-price__row">
        <img class="store-logo" alt="{store}">
        <span class="store-price">{price}</span>
    </div>
    """


def test_price_with_thousands_separator_is_parsed():
    html = make_product_html(
        make_price_row("Maxi", "1.410,00 RSD")
    )

    result = find_the_prices(html)

    assert result is not None
    assert len(result) == 1

    store, price, product, category = result[0]

    assert store == "Maxi"
    assert price == pytest.approx(1410.00)
    assert product == "Čokolada TEST 100g"
    assert category == "Slatkiši"


def test_price_without_thousands_separator_is_parsed():
    html = make_product_html(
        make_price_row("Maxi", "1410,00 RSD")
    )

    result = find_the_prices(html)

    assert result is not None
    assert result[0][1] == pytest.approx(1410.00)


def test_invalid_price_does_not_stop_other_rows():
    html = make_product_html(
        make_price_row("Idea", "Nema na stanju"),
        make_price_row("Maxi", "999,99 RSD"),
    )

    result = find_the_prices(html)

    assert result is not None
    assert len(result) == 1

    store, price, _, _ = result[0]

    assert store == "Maxi"
    assert price == pytest.approx(999.99)


def test_missing_price_span_does_not_crash():
    html = make_product_html(
        """
        <div class="store-price__row">
            <img class="store-logo" alt="Roda">
        </div>
        """,
        make_price_row("Maxi", "250,50 RSD"),
    )

    result = find_the_prices(html)

    assert result is not None
    assert len(result) == 1
    assert result[0][0] == "Maxi"
    assert result[0][1] == pytest.approx(250.50)


def test_missing_store_alt_uses_unknown():
    html = make_product_html(
        """
        <div class="store-price__row">
            <img class="store-logo">
            <span class="store-price">100,00 RSD</span>
        </div>
        """
    )

    result = find_the_prices(html)

    assert result is not None
    assert result[0][0] == "unknown"
    assert result[0][1] == pytest.approx(100.00)


def test_empty_html_returns_none():
    assert find_the_prices("") is None
    assert find_the_prices(None) is None