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
    await update.message.reply_text("Hello! Thanks for using our Bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Please type something so I can search it for you")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

#responses

def handle_request(text: str) -> str:
    print("The Message has been received successfully")
    return text


if __name__ == "__main__":
    pass
    """get_the_lowest_price_to_notify()"""