# Grocery Notificator

Grocery Notificator is a Python application for searching and comparing grocery prices from Serbian stores through a Telegram bot.

Made for my parents and other elderly people who do not want an app for every store and a bunch of unnecessary notifications.

The application collects product data, stores price history in a SQLite database, and allows users to search for products using natural multi-word queries.

## Features

* Product crawling and web scraping
* Grocery price comparison
* SQLite database
* Product price history
* Multi-word product search
* Telegram bot interface
* Links to available products and stores

## How It Works

```text
Cenoteka
   ↓
Crawler
   ↓
Scraper
   ↓
SQLite Database
   ↓
Product Search
   ↓
Telegram Bot
   ↓
User
```

The crawler discovers product pages, while the scraper extracts product information and prices.

The data is stored in SQLite, including historical prices.

Users can then search for products through the Telegram bot, for example:

```text
jaja 10 kom
```

The bot returns matching products sorted by price.

## Tech Stack

* Python
* SQLite
* BeautifulSoup
* Requests
* Pandas
* python-telegram-bot
* python-dotenv

## Project Structure

```text
grocery-notificator/
│
├── crawler/
│   └── cenoteka_crawler.py
│
├── scraper/
│   └── cenoteka_scraper.py
│
├── data/
│   └── database.py
│
├── processors/
│
├── notifications/
│   └── telegram_bot.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/crnogoracmilos/grocery-notificator.git
cd grocery-notificator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
TELEGRAM_BOT_TOKEN=your_bot_token
```

Then run the application.

```bash
python main.py
```

## Roadmap

Planned features:

* Price drop notifications
* User-specific tracked products
* Improved product matching
* More stores and data sources
* Automated scraping
* Docker support
* Automated testing and CI/CD

## Status

The project is currently under active development.
