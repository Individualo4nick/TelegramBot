from telegram import Update, KeyboardButton , ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import db
import datetime


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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Action canceled ")
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

purchase_data = []
async def add_purchase(update, context):
    purchase_data.append(datetime.date.today())
    if not db.user_has_family(update.message.chat.username):
        await context.bot.send_message ( chat_id=update.effective_chat.id ,
                                         text="You must be in the family to add purchases" )
        return ConversationHandler.END
    purchase_types = [
        KeyboardButton("🚌 Transport"),
        KeyboardButton("✈ Trips"),
        KeyboardButton("🛒 Supermarkets"),
        KeyboardButton("🍴 Restaurants"),
        KeyboardButton("🎓 Education"),
        KeyboardButton("👕 Clothes"),
        KeyboardButton("🏥 Health and beauty"),
        KeyboardButton("🏄 Hobby"),
        KeyboardButton("🏠 Communications, Internet, etc.")
    ]
    family_id = db.get_family_id(update.message.chat.username)
    purchase_data.append(update.message.chat.username)
    purchase_data.append(family_id[0])
    reply_markup = ReplyKeyboardMarkup(build_menu(purchase_types, 3), one_time_keyboard=True)
    await context.bot.send_message ( chat_id=update.effective_chat.id ,
                                     text="Choose purchase type", reply_markup=reply_markup)
    return 1

async def enter_price(update, context):
    purchase_data.append(update.message.text[2:])
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Enter purchase price in rubles")
    return 2

async def save_purchase(update,context):
    purchase_data.append(int(update.message.text))
    db.add_purchase(purchase_data)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Purchase successful added")
    return ConversationHandler.END

def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu



