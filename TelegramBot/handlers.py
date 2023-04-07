from telegram import Update, KeyboardButton , ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
import db
import datetime

class FamilyInfo:
    def __init__(self):
        self.login = ""
        self.password = ""
        self.family_name = ""

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
    context.user_data["family"] = FamilyInfo()
    user_has_family = db.user_has_family(update.message.chat.username)
    if user_has_family == -1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You are not registered. Register to create a family")
        return ConversationHandler.END
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Enter LOGIN for your family")
    return 1


async def family_login(update, context):
    print("im in login")
    result = db.check_family_login(update.message.text)


    # Family with this id exist
    if result == -1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Family with such login exists. Enter login again")
        return 1
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Cool! Next, enter password for your family account")
        context.user_data["family"].login = update.message.text
        return 2


async def family_password(update, context):
    password = update.message.text
    if len(password) > 8 and ("".join(filter(str.isdigit, password)) != ""):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="We save your password. Enter your family name")
        context.user_data["family"].password = password
        return 3
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Password must be more than 8 characters long and must contain numbers")
        return 2


async def family_name(update, context):
    name = update.message.text
    context.user_data["family"].family_name = name
    db.add_family(context.user_data["family"], update.message.chat.username)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="You have successfully raised a family")
    return ConversationHandler.END

purchase_data = []
async def add_purchase(update, context):
    global purchase_data
    purchase_data = []
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
    await context.bot.send_message (chat_id=update.effective_chat.id ,
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

def data_conversion(spendings_category, spendings_price):
    """
    Converts the information from the database into a dictionary
    :param spendings_category: categories of goods on request in the database
    :param spendings_price: price of goods on request in the database
    :return: converted data
    """
    spendings_price_category = {}
    unique_spendings_category = tuple(set(spendings_category))
    for i in range(len(unique_spendings_category)):
        spendings_price_category[unique_spendings_category[i][0]] = 0
        for j in range(len(spendings_price)):
            if unique_spendings_category[i][0] == spendings_category[j][0]:
                spendings_price_category[unique_spendings_category[i][0]] += spendings_price[j][0]
    return spendings_price_category

def get_spending_period(family_id, period):
    """
    Getting information about period expenses by category and family members
    :param family_id: id of family
    :param period: getting information for the day, week or month
    :return: the message that the bot will display
    """
    result = ''

    if period == 'Month':
        now = datetime.datetime.now()
        now = now.month
    elif period == 'Week':
        now = datetime.datetime.today()
        now = now.isocalendar()[1]
    elif period == 'Day':
        now = datetime.datetime.now()
        now = now.day
    spendings_member = db.get_period_members(period, now, family_id)
    unique_spendings_member = tuple(set(spendings_member))
    members = {}
    for i in range(len(unique_spendings_member)):
        spendings_price, spendings_category = db.get_spend_member(period, now, unique_spendings_member[i][0], family_id)
        spendings_price_category = data_conversion(spendings_category, spendings_price)
        members[unique_spendings_member[i][0]] = spendings_price_category
    spendings_price, spendings_category = db.get_spend(period, now, family_id)
    spendings_price_category = data_conversion(spendings_category, spendings_price)
    purchase = f'This {period} you made purchases in the following categories:\n\n'
    result += purchase
    for category in spendings_price_category.keys():
        purchase = f'{category}: for the amount of {spendings_price_category[category]} rubles \n\n'
        result += purchase
    result += "=====================================================\n\n"
    for member in members.keys():
        purchase = f'User {member} made purchases this {period} in the following categories:\n\n'
        result += purchase
        for category in members[member].keys():
            purchase = f'{category} category for the amount of {members[member][category]} rubles \n \n'
            result += purchase
    return result


async def choose_period(update, context):
    """
    Select the period for which you want to display information
    """
    family_id = db.get_family_id(update.message.chat.username)
    if family_id:
        period_types = [
            KeyboardButton("Month"),
            KeyboardButton("Week"),
            KeyboardButton("Day")
        ]
        reply_markup = ReplyKeyboardMarkup(build_menu(period_types, 1), one_time_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Choose period", reply_markup=reply_markup)
        return 1
    else:
        result = "You are not a member of the family. Add to or start a family."
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result)
        return -1

async def get_spending(update, context):
    """
    Getting information for a certain period and outputting it
    """
    family_id = db.get_family_id(update.message.chat.username)[0]
    if update.message.text == 'Month':
        result = get_spending_period(family_id, update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result)
    if update.message.text == 'Week':
        result = get_spending_period(family_id, update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result)
    if update.message.text == 'Day':
        result = get_spending_period(family_id, update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=result)
    return ConversationHandler.END
