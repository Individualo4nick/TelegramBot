"""
 This is module bot configuration
"""
import logging
import json
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler
import TelegramBot.handlers as handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def config_bot():
    """
    Commands and configs of telegram bot
    """
    with open("../config.json") as json_data:
        data = json.load(json_data)

    application = ApplicationBuilder().token(data["Token"]).build()

    # Handlers
    start_handler = CommandHandler('start', handlers.start)
    # Add conversation handler with the states

    conv_registration_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Regex("Registration"), callback=handlers.reg)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.get_name)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    conv_create_family_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Regex("Create new family"), callback=handlers.create_family)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.family_login)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.family_password)],
            3: [MessageHandler(filters=filters.TEXT, callback=handlers.family_name)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    conv_login_family_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Regex("Join to family"), callback=handlers.login_to_family)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.family_login_to_enter)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.family_password_to_enter)]
        },
        fallbacks = [CommandHandler("cancel", handlers.cancel)],
    )
    conv_add_purchase_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Regex("Add purchase"), callback=handlers.add_purchase)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.enter_price)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.save_purchase)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    leave_family_handler = MessageHandler(filters=filters.Regex("Leave from family"), callback=handlers.leave_from_family)
    login_family_handler = MessageHandler(filters=filters.Regex('Join to family'), callback=handlers.login_to_family)
    add_purchase_handler = MessageHandler(filters=filters.Regex('Add purchase'), callback=handlers.add_purchase)
    create_family_handler = MessageHandler(filters=filters.Regex('Create new family'), callback=handlers.create_family)
    registration_handler = MessageHandler(filters=filters.Regex("Registration"), callback=handlers.reg)
    cancel_registration_handler = CommandHandler("cancel", handlers.cancel)
    conv_get_handler = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Regex("Get statistics"), callback=handlers.choose_period)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.get_spending)],
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    get_handler = MessageHandler(filters=filters.Regex('Get statistics'), callback=handlers.get_spending)

    get_members_handler = MessageHandler(filters=filters.Regex('Get family members'), callback=handlers.get_members)

    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)



    # Link handlers
    application.add_handler(start_handler)


    # Create family
    application.add_handler(conv_create_family_handler)
    application.add_handler(create_family_handler)

    # User registration
    application.add_handler(conv_registration_handler)
    application.add_handler(registration_handler)

    # Add purchase
    application.add_handler(conv_add_purchase_handler)
    application.add_handler(add_purchase_handler)

    # Get spendings
    application.add_handler(conv_get_handler)
    application.add_handler(get_handler)

    # Get family members
    application.add_handler(get_members_handler)

    # Login to family
    application.add_handler(conv_login_family_handler)
    application.add_handler(login_family_handler)
    # Leave
    application.add_handler(leave_family_handler)
    # Other handlers
    application.add_handler(cancel_registration_handler)
    application.add_handler(unknown_handler)


    application.run_polling()

if __name__ == '__main__':
    config_bot()
