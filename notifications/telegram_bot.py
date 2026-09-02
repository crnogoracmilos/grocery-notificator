from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Final
import os
from dotenv import load_dotenv

TELEGRAM_TOKEN: Final = f"{load_dotenv("TELEGRAM_TOKEN")}"
BOT_USERNAME: Final = '@citac_namirnica_bot'

CHAT_ID = "5623598376"

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for using our Bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please type something so I can search it for you")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

#responses

async def handle_response(text: str) -> str:
    print("The Message has been received successfully")
    return text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f"User ({update.message.chat.id}): {text}")
    response: str = handle_request(text)
    print("Bot", response)




if __name__ == "__main__":
    pass
    """get_the_lowest_price_to_notify()"""