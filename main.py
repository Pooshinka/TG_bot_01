import asyncio
import logging

from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler

import Sqlite3_tg
from app.handlers import start, help_command, stop, close_keyboard, show_data, send_picture, \
    save_message, button, give_photo
from config import TOKEN

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    persistence = Sqlite3_tg.SqlitePersistence()
    application = Application.builder().token(TOKEN).persistence(persistence).build()

    #
    # application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("send_picture", send_picture))
    application.add_handler(CommandHandler("give_photo", give_photo))

    application.add_handler(CallbackQueryHandler(button))

    show_data_handler = CommandHandler("show_data", show_data)
    application.add_handler(show_data_handler)
    application.add_handler(MessageHandler(filters=filters.ALL, callback=save_message))  # (3)
    application.run_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
