from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final
import os
from dotenv import load_dotenv

TELEGRAM_TOKEN: Final = "8947475366:AAF_G51H8wZvZphiM5NG4CS6wnl76MLEAM8"
BOT_USERNAME: Final = '@citac_namirnica_bot'

CHAT_ID = "5623598376"

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for usinXg our Bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please type something so I can search it for you")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

#responses



"""def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id" : CHAT_ID,
        "text" : text,
        "parse_mode" : "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("The message has been sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"There was an error while sending a message to the Telegram bot: {e}")

def get_the_lowest_price_to_notify():
    current_file = Path(__file__).resolve()
    db_path = current_file.parent.parent / 'data' / 'groceries.db'

    try:
        with sqlite3.connect(db_path) as connection:
            data = pd.read_sql("SELECT * FROM groceries WHERE in_stock = 1", connection)

            if data.empty:
                print("The Database is either empty or does not exist")
                return
            lowest_price = find_lowest()
            message = "<b>The lowest prices for selected items: </b>\n\n"
            for index, values in lowest_price.head(5).iterrows():
                message += f"• <b>{values['grocery']}</b> u {values['store']} - {values['price']} RSD\n"
                message += f"  <a href='{values['url']}'>Link to the grocery</a>\n\n"
            send_message(message)
    except Exception as e:
        print(f"Error with database: {e}")"""

if __name__ == "__main__":
    pass
    """get_the_lowest_price_to_notify()"""