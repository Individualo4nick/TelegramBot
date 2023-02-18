import logging
import json
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import MySQLdb

import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, i didn't understand that command")

async def create_family(update, context):
    params = ' '.join(context.args).split(' ')
    db.add_family(params)
    await update.message.reply_text("Your data saved")

if __name__ == '__main__':

    with open("config.json") as json_data:
        data = json.load(json_data)

    application = ApplicationBuilder().token(data["Token"]).build()
    start_handler = CommandHandler('start', start)
    create_family_handler = CommandHandler('create', create_family)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(create_family_handler)
    application.add_handler(unknown_handler)

    application.run_polling()