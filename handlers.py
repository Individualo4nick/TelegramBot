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

    db.register(update.message.text, update.message.chat.username)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Your data saved")
    return ConversationHandler.END


async def cancel(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="You cancel registration")
    return ConversationHandler.END




family_info = []


async def create_family(update, context):
    user_has_family = db.user_has_family(update.message.chat.username)
    if user_has_family == -1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Register to create a family")
        return ConversationHandler.END
    if user_has_family == -2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are already in the family. Leave the current family to create a new one")
        return ConversationHandler.END
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter LOGIN for your family")
    return 1


async def family_login(update, context):
    print("im in login")
    result = db.check_family_login(update.message.text)

    if result == -1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Family with such login exists. Enter login again")
        return 1
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Cool! Next, enter password for your family account")
        family_info.append(update.message.text)
        return 2


async def family_password(update, context):
    password = update.message.text
    if len(password) > 8 and ("".join(filter(str.isdigit, password)) != ""):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="We save your password. Enter your family name")
        family_info.append(password)
        return 3
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Password must be more than 8 characters long and must contain numbers")
        return 2


async def family_name(update, context):
    name = update.message.text
    family_info.append(name)
    db.add_family(family_info, update.message.chat.username)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="You have successfully raised a family")
    return ConversationHandler.END

