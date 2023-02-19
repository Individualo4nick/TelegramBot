import logging
import json
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler
import db
import MySQLdb
import handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    with open("config.json") as json_data:
        data = json.load(json_data)

    application = ApplicationBuilder().token(data["Token"]).build()

    # Handlers
    start_handler = CommandHandler('start', handlers.start)
    create_family_handler = CommandHandler('create', handlers.create_family)
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_registration_handler = ConversationHandler(
        entry_points=[CommandHandler("reg", handlers.reg)],
        states={
            1: [MessageHandler(filters=filters.TEXT, callback=handlers.get_name)]
        },
        fallbacks=[CommandHandler("cancel", handlers.cancel)],
    )
    registration_handler = CommandHandler("reg", handlers.reg)
    cancel_registration_handler = CommandHandler("cancel", handlers.cancel)
    unknown_handler = MessageHandler(filters.COMMAND, handlers.unknown)



    # Link handlers
    application.add_handler(start_handler)
    application.add_handler(create_family_handler)
    application.add_handler(conv_registration_handler)
    application.add_handler(registration_handler)
    application.add_handler(cancel_registration_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
