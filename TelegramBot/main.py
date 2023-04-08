import logging
import json
from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler

import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    with open("../config.json") as json_data:
        data = json.load(json_data)

    application = ApplicationBuilder().token(data["Token"]).build()

    # Handlers
    start_handler = CommandHandler('start', handlers.start)
    # Add conversation handler with the states
    conv_registration_handler = ConversationHandler(
        entry_points=[CommandHandler("reg", handlers.reg)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.get_name)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    conv_create_family_handler = ConversationHandler(
        entry_points=[CommandHandler("create", handlers.create_family)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.family_login)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.family_password)],
            3: [MessageHandler(filters=filters.TEXT, callback=handlers.family_name)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    conv_login_family_handler = ConversationHandler(
        entry_points=[CommandHandler("login", handlers.login_to_family)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.family_login_to_enter)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.family_password_to_enter)]
        },
        fallbacks = [CommandHandler("cancel", handlers.cancel)],
    )
    conv_add_purchase_handler = ConversationHandler(
        entry_points=[CommandHandler("addpurchase", handlers.add_purchase)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.enter_price)],
            2: [MessageHandler(filters=filters.TEXT, callback=handlers.save_purchase)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    login_family_handler = CommandHandler('login', handlers.login_to_family)
    add_purchase_handler = CommandHandler('addpurchase', handlers.add_purchase)
    create_family_handler = CommandHandler('create', handlers.create_family)
    registration_handler = CommandHandler("reg", handlers.reg)
    cancel_registration_handler = CommandHandler("cancel", handlers.cancel)
    conv_get_handler = ConversationHandler(
        entry_points=[CommandHandler("get", handlers.choose_period)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.get_spending)],
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    get_handler = CommandHandler('get', handlers.get_spending)
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

    # Login to family
    application.add_handler(conv_login_family_handler)
    application.add_handler(login_family_handler)
    # Other handlers
    application.add_handler(cancel_registration_handler)
    application.add_handler(unknown_handler)


    application.run_polling()
