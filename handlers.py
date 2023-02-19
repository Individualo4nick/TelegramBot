from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, i didn't understand that command")


async def reg(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="What is your name?")
    return 1

async def get_name(update, context):
    print(update.message.text, update.message.chat.username)

    db.register(update.message.text, update.message.chat.username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Your data saved")
    return ConversationHandler.END


async def cancel(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You cancel registration")
    return ConversationHandler.END


async def create_family(update, context):
    params = ' '.join(context.args).split(' ')
    db.add_family(params)
    await update.message.reply_text("Your data saved")
