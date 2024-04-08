import logging
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,\
    KeyboardButton
from telegram.ext import Application, Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
    filters,
    CallbackContext,
    BasePersistence,
    PersistenceInput
)

import asyncio
from config import TOKEN


reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)



async def echo(update, context):
    pass


# /start (начало работы программы)
async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        f"Добро пожаловать {user.mention_html()}! Меня зовут Ньютон. Если в желаете хотите открыть меню, то"
        f" напишите /menu. Если вы хотите прекратить со мной общение на напишите /stop",
    )


# /help (справочный материал)
async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def menu_command(update, context):
    await update.message.reply_text("Открыто меню:", reply_markup=markup)


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


async def close_keyboard(update, context):
    await update.message.reply_text("Меню закрыто", reply_markup=ReplyKeyboardRemove())

async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the gathered info."""
    def _read_messages(chat_messages):
        return '\n'.join([f'{x["message_ts"]}: {x["message"]}' for x in chat_messages])

    messages = [f"\n{key}:\n{_read_messages(value)}" for key, value in context.chat_data.items()]
    facts = '\n'.join(messages)
    await update.message.reply_text(
        f"This is what you already told me: {facts}"
    )

async def save_message(update: Update, context: CallbackContext) -> None:
    if 'messages' not in context.chat_data:
        context.chat_data['messages'] = []
    context.chat_data['messages'].append({'message': update.message.text, 'message_ts': update.message.date.timestamp()}) # (4)