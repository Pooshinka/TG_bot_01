
import logging
import asyncio
from telegram.ext import Application, MessageHandler, filters, CommandHandler, Updater, CallbackQueryHandler, \
    BasePersistence, PersistenceInput
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update
from config import TOKEN
from app.handlers import start, help_command, menu_command, stop, address, phone, site, work_time, close_keyboard, show_data, \
    save_message
import Sqlite3_tg


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
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.add_handler(CommandHandler("phone", phone))
    application.add_handler(CommandHandler("site", site))
    application.add_handler(CommandHandler("work_time", work_time))
    application.add_handler(CommandHandler("close_keyboard", close_keyboard))
    show_data_handler = CommandHandler("show_data", show_data)
    application.add_handler(show_data_handler)
    application.add_handler(MessageHandler(filters=filters.ALL, callback=save_message))  # (3)
    application.run_polling()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')