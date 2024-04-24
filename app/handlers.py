import logging
from random import randint

import telegram
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

level = 0
import asyncio
from config import TOKEN
import requests

question_kynematic = ['Какое изменение, происходящее с телами, можно считать механическим движением:',
                      'Какое изменение, происходящее с телами, можно считать механическим движением:',
                      'Какое изменение, происходящее с телами, можно считать механическим движением:',
                      'Какое изменение, происходящее с телами, можно считать механическим движением',
                      'Скорость автомобиля увеличилась в 2 раза. При этом тормозной путь:'
                      ]
question_temp = ['К тепловым явлениям относятся:',
                 'В каком из перечисленных веществ теплопередача происходит главным образом путем теплопроводности:',
                 'Количество теплоты, необходимое для нагревания тела, зависит от:',
                 'Какое физическое явление лежит в основе устройства и работы ртутного термометра:',
                 'Какое движение молекул и атомов в твердом состоянии называется тепловым:'
                 ]
question_dynamics = ['Точка приложения равнодействующей сил тяжести, действующих на все части тела называется …',
                    'Грузик массой 2 кг тянут вверх верёвкой с ускорением 10 м/с2. Определить силу натяжения верёвки',
                    'Выберите направление вектора ускорения, с которым движется камень, если его кинули вверх с начальной скоростью v1',
                    'Закон инерции открыл …',
                    'Какой вид имеет график зависимости скорости движения тела от времени v = v(t) при равномерном движении?',
                    ]

otvet_kynematic = [{'движение лодки относительно берега': 'Verno', 'таяние льда': 'ne verno', 'кипение воды': 'ne verno',},
                   {'таяние льда': 'ne verno', 'волны, образующиеся на поверхности воды': 'Verno', 'кипение воды': 'ne verno',},
                   {'кипение воды': 'ne verno', 'таяние льда': 'ne verno', 'колебания поршня в двигателе внутреннего сгорания': 'Verno',},
                   {'колебания струны': 'Verno', 'таяние льда': 'ne verno', 'кипение воды': 'ne verno',},
                   {'не изменился': 'ne verno', 'увеличился в 2 раза': 'ne verno', 'увеличился в 4 раза': 'Verno',}
                   ]

tasks_kynematic = [['движение лодки относительно берега', 'таяние льда', 'кипение воды',],
                   ['таяние льда', 'волны, образующиеся на поверхности воды', 'кипение воды',],
                   ['кипение воды', 'таяние льда', 'колебания поршня в двигателе внутреннего сгорания',],
                   ['колебания струны', 'таяние льда', 'кипение воды',],
                   ['не изменился', 'увеличился в 2 раза', 'увеличился в 4 раза']
                   ]

otvet_dynamics = [{'Геометрическим центром': 'ne verno', 'Центром масс': 'ne verno', 'Центром тяжести': 'Verno'},
                  {'40 Н': 'Verno', '20 Н': 'ne verno', '10 Н': 'ne verno'},
                  {'вертикально вверх': 'ne verno', 'вертикально вниз': 'Verno', 'горизонтально': 'ne verno'},
                  {'Ньютон': 'ne verno', 'Коперник': 'ne verno', 'Галилей': 'Verno'},
                  {'горизонтальный отрезок ': 'Verno', 'вертикальный отрезок': 'ne verno', 'наклонный отрезок': 'ne verno'}]

tasks_dynamics = [['Геометрическим центром', 'Центром масс', 'Центром тяжести'],
                  ['40 Н', '20 Н', '10 Н'],
                  ['вертикально вверх', 'вертикально вниз', 'горизонтально'],
                  ['Ньютон', 'Коперник', 'Галилей'],
                  ['горизонтальный отрезок', 'вертикальный отрезок', 'наклонный отрезок']]

tasks_temp = [['движение Земли вокруг Солнца', 'падение мяча на землю', 'нагревание воды в чайнике'],
              ['вакуум', 'кирпич', 'воздух'],
              ['рода вещества, из которого состоит тело, массы тела, изменения его температуры', 'плотности вещества, из которого состоит тело, массы тела, изменения его температуры', 'рода вещества, из которого состоит тело, массы тела, его температуры'],
              ['расширение жидкости при нагревании', 'конвекция в жидкости при нагревании', 'плавление твердого тела при нагревании'],
              ['упорядоченное движение частиц со скоростью, пропорциональной температуре', 'беспорядочное движение частиц во всевозможных направлениях с различными скоростями', 'колебательное движение частиц в различных направлениях около определенных положений равновесия']]


otvet_temp = [{'движение Земли вокруг Солнца': 'ne verno', 'падение мяча на землю': 'ne verno', 'нагревание воды в чайнике': 'Verno'},
              {'вакуум': 'ne verno', 'кирпич': 'Verno', 'воздух': 'ne verno'},
              {'рода вещества, из которого состоит тело, массы тела, изменения его температуры': 'ne verno', 'плотности вещества, из которого состоит тело, массы тела, изменения его температуры': 'ne verno', 'рода вещества, из которого состоит тело, массы тела, его температуры': 'Verno'},
              {'расширение жидкости при нагревании': 'Verno', 'конвекция в жидкости при нагревании': 'ne verno', 'плавление твердого тела при нагревании': 'ne verno'},
              {'упорядоченное движение частиц со скоростью, пропорциональной температуре': 'ne verno', 'беспорядочное движение частиц во всевозможных направлениях с различными скоростями': 'ne verno', 'колебательное движение частиц в различных направлениях около определенных положений равновесия': 'Verno'},]




images_hz = ['https://disk.yandex.ru/i/UgxbIntO35_Afw', 'https://disk.yandex.ru/i/UgxbIntO35_Afw']

kinematic = ['https://disk.yandex.ru/i/UgxbIntO35_Afw', 'https://disk.yandex.ru/i/UgxbIntO35_Afw',
             'https://disk.yandex.ru/i/SG30BTPrQR4M9g', 'https://disk.yandex.ru/i/46hc-XILyY7bpg',
             'https://disk.yandex.ru/i/dc0i11aUhmdYBA', 'https://disk.yandex.ru/i/Ab_hdI8L-aUCgQ',
             'https://disk.yandex.ru/i/KhGpsAjsW1Whvw', 'https://disk.yandex.ru/i/me7NfNSbjF7m9g']

images_temp = ['https://disk.yandex.ru/i/VTkVBo8NRgTzuA', 'https://disk.yandex.ru/i/h8ekJV20ZtgnBw', 'https://disk.yandex.ru/i/X_1UZx_G-CejXA']


dinamika = ['https://disk.yandex.ru/i/zg5GgIaI-98KOA',
'https://disk.yandex.ru/i/RCf30McZeL8LVg',
'https://disk.yandex.ru/i/8P5bYeKgkw0JYA',
'https://disk.yandex.ru/i/n1ASr0jreNkiMQ',
'https://disk.yandex.ru/i/wVvfVpaovRrV7Q']
txt = ['Движение точки называется равномерным, если она за любые равные промежутки времени проходит одинаковые пути.',
       'Движение вдоль прямой с постоянным ускорением, при котором модуль скорости увеличивается, называется прямолинейным равноускоренным движением, а прямолинейное движение с постоянным ускорением, при котором модуль скорости уменьшается, называется равнозамедленным.']
spisok = []
counter = 0



async def echo(update, context):
    pass


async def send_picture(update, context):
    await context.bot.send_photo(update.message.chat.id, photo='https://disk.yandex.ru/i/UgxbIntO35_Afw')



async def give_photo(upadte, context):
    chat_id = '430271094'
    token = TOKEN
    msg = "Send text with photo 😉"
    img_uri = "https://disk.yandex.ru/i/UgxbIntO35_Afw"
    telegram_msg = requests.get(
        f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')


# /start (начало работы программы)
async def start(update, context):
    global level
    level = 0
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    chat_id = update.message.chat_id
    token = TOKEN
    msg = "😉"
    img_uri = "https://disk.yandex.ru/i/oyWGWVusZyVEOw"
    telegram_msg = requests.get(
        f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
    await update.message.reply_html(
        f"Добро пожаловать {user.mention_html()}! Меня зовут Ньютон. Если в желаете ознакомитсься с доступным спискомм команд, "
        f"то напишите /help",
    )
    inline_keyboard_start = [
        [InlineKeyboardButton("Механика", callback_data="mechanics")],
        [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
    ]

    inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

    await update.message.reply_text("Выберите интересующую вас тему:", reply_markup=inline_markup)



# /help (справочный материал)
async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Список команд:\n"
                                    "/start - начать работу бота\n"
                                    "/reply_menu - вызов reply меню\n"
                                    '/inline_menu - вызов inline меню\n'
                                    "/stop - прекращение работы программы\n"
                                    "/close - закрывает меню или клавиатуру"
                                    "/send_picture - показывает фото")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global level, tasks_kynematic, counter, question_kynematic, otvet_kynematic
    query = update.callback_query
    await query.answer()
    if level == 0:
        if query.data == 'mechanics':
            spisok.append('mechanics')
            level = 1
            query1 = update.callback_query
            await query1.answer()
            inline_keyboard = [
            [InlineKeyboardButton("Кинематика", callback_data="kynematic")],
            [InlineKeyboardButton("Динамика", callback_data="dynamics")],
            [InlineKeyboardButton("Назад", callback_data="go_back")],
        ]

            inline_markup = InlineKeyboardMarkup(inline_keyboard)
            await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
        elif query.data == 'temp':
            spisok.append('temp')
            level = 1
            query1 = update.callback_query
            await query1.answer()
            inline_keyboard = [
            [InlineKeyboardButton("Виды теплопередач", callback_data="teplop")],
            [InlineKeyboardButton("Строение вещества", callback_data="stroyenie")],
            [InlineKeyboardButton("Тепловое движение", callback_data="teplo_dvg")],
            [InlineKeyboardButton("Пройти тест", callback_data="test_temp")],
            [InlineKeyboardButton("Назад", callback_data="go_back")]
        ]

            inline_markup = InlineKeyboardMarkup(inline_keyboard)
            await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 1:
        if spisok[-1] == 'mechanics':
            if query.data == 'dynamics':
                spisok.append('dynamics')
                await query.message.reply_text('Динамика')
                level = 2
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Первый закон Ньютона", callback_data="first_newton")],
                    [InlineKeyboardButton("Второй закон Ньютона", callback_data="second_newton")],
                    [InlineKeyboardButton("Третий закон Ньютона", callback_data="tretiy_newton")],
                    [InlineKeyboardButton("Силы в природе", callback_data="sili_v_prirode")],
                    [InlineKeyboardButton("Виды деформации", callback_data="vidi_deform")],
                    [InlineKeyboardButton("Пройти тест", callback_data="test_dynamics")],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
            if query.data == 'go_back':
                level = 0
                inline_keyboard_start = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)

    if level == 1:
        if spisok[-1] == 'mechanics':
            if query.data == 'kynematic':
                level = 2
                spisok.append('kynematic')
                query1 = update.callback_query
                await query1.answer()
                await query1.message.reply_text('Кинематика')
                inline_keyboard = [
                    [InlineKeyboardButton("Равномерное движение", callback_data="ravn")],
                    [InlineKeyboardButton("Равноускоренное движение", callback_data="ravnousk")],
                    [InlineKeyboardButton("Поступательное движение", callback_data="postup")],
                    [InlineKeyboardButton("Вращательное движение", callback_data="vrashateln")],
                    [InlineKeyboardButton("Движение с постоянным ускорением", callback_data="dvgspostus")],
                    [InlineKeyboardButton("Мгновенная и средняя скорость", callback_data="mgnov")],
                    [InlineKeyboardButton("Сложение скоростей", callback_data="slogenie")],
                    [InlineKeyboardButton("Ускорение", callback_data="uskor")],
                    [InlineKeyboardButton("Пройти тест", callback_data="test_kyn")],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)
            if query.data == 'go_back':
                level = 0
                inline_keyboard_start = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)
    if level == 1:
        if spisok[-1] == 'temp':
            if query.data == 'teplop':
                await query.message.reply_text('Виды теплопредачи')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Виды теплопредачи 😉"
                img_uri = images_temp[0]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                inline_keyboard_start = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)
    if level == 1:
        if spisok[-1] == 'temp':
            if query.data == 'stroyenie':
                await query.message.reply_text('Строение вещества')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Строение вещества 😉"
                img_uri = images_temp[1]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                inline_keyboard_start = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)
    if level == 1:
        if spisok[-1] == 'temp':
            if query.data == 'teplo_dvg':
                await query.message.reply_text('Тепловое движение молекул')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Тепловое движение молекул 😉"
                img_uri = images_temp[2]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                inline_keyboard_start = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard_start)

                await query.edit_message_text("Выберите интересующую вас тему:", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'first_newton':
                await query.message.reply_text('Первый закон Ньютона')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Первый закон Ньютона 😉"
                img_uri = dinamika[0]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'second_newton':
                await query.message.reply_text('Второй закон Ньютона')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Второй закон Ньютона 😉"
                img_uri = dinamika[1]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'tretiy_newton':
                await query.message.reply_text('Третий закон Ньютона')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Третий закон Ньютона 😉"
                img_uri = dinamika[2]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'sili_v_prirode':
                await query.message.reply_text('Силы в природе')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Силы в природе 😉"
                img_uri = dinamika[3]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'vidi_deform':
                await query.message.reply_text('Виды деформации')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Виды деформации 😉"
                img_uri = dinamika[4]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)


# КИНЕМАТИКА
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'ravn':
                await query.message.reply_text('Равномерное движение')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Равномерное движение 😉"
                img_uri = kinematic[0]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'ravnousk':
                await query.message.reply_text('Равноускоренное движение')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Равноускоренное движение 😉"
                img_uri = kinematic[1]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)

    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'postup':
                await query.message.reply_text('Поступательное движение')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Поступательное движение 😉"
                img_uri = kinematic[2]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)

    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'vrashateln':
                await query.message.reply_text('Вращательное движение')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Вращательное движение 😉"
                img_uri = kinematic[3]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'dvgspostus':
                await query.message.reply_text('Движение с постоянным ускорением')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Движение с постоянным ускорением 😉"
                img_uri = kinematic[4]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'mgnov':
                await query.message.reply_text('Мгновенная и средняя скорость')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Мгновенная и средняя скорость 😉"
                img_uri = kinematic[5]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'slogenie':
                await query.message.reply_text('Сложение скоростей')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Сложение скоростей 😉"
                img_uri = kinematic[6]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'uskor':
                await query.message.reply_text('Ускорение')
                chat_id = query.message.chat_id
                token = TOKEN
                msg = "Ускорение 😉"
                img_uri = kinematic[7]
                telegram_msg = requests.get(
                    f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}&caption={msg}&photo={img_uri}')
            if query.data == 'go_back':
                level = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'kynematic':
            if query.data == 'test_kyn':
                spisok.append('test_kyn')
                level = 3
                await query.message.reply_text('Tecт')
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_kynematic[counter][0], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][0]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][1], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][1]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][2], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_kynematic[counter], reply_markup=inline_markup)
    if level == 3:
        if spisok[-1] == 'test_kyn':
            if query.data == 'Verno':
                counter += 1
                await query.message.reply_text('Верно✅')
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_kynematic[counter][0], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][0]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][1], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][1]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][2], callback_data=otvet_kynematic[counter][tasks_kynematic[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_kynematic[counter], reply_markup=inline_markup)

            if query.data == 'ne verno':
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_kynematic[counter][0],
                                          callback_data=otvet_kynematic[counter][tasks_kynematic[counter][0]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][1],
                                          callback_data=otvet_kynematic[counter][tasks_kynematic[counter][1]])],
                    [InlineKeyboardButton(tasks_kynematic[counter][2],
                                          callback_data=otvet_kynematic[counter][tasks_kynematic[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_kynematic[counter] + ' Неверно❌', reply_markup=inline_markup)
            if counter == 5:
                counter = 0
                await query.message.reply_text('Поздравляю, ты прошел тест!🎉')

            if query.data == 'go_back':
                level = 0
                counter = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'dynamics':
            if query.data == 'test_dynamics':
                spisok.append('test_dynamics')
                level = 3
                await query.message.reply_text('Tecт')
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_dynamics[counter][0], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][0]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][1], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][1]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][2], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]
                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_dynamics[counter], reply_markup=inline_markup)
    if level == 3:
        if spisok[-1] == 'test_dynamics':
            if query.data == 'Verno':
                counter += 1
                query1 = update.callback_query
                await query.message.reply_text('Верно✅')
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_dynamics[counter][0],
                                          callback_data=otvet_dynamics[counter][tasks_dynamics[counter][0]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][1],
                                          callback_data=otvet_dynamics[counter][tasks_dynamics[counter][1]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][2],
                                          callback_data=otvet_dynamics[counter][tasks_dynamics[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_dynamics[counter], reply_markup=inline_markup)

            if query.data == 'ne verno':
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_dynamics[counter][0], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][0]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][1], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][1]])],
                    [InlineKeyboardButton(tasks_dynamics[counter][2], callback_data=otvet_dynamics[counter][tasks_dynamics[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_dynamics[counter] + ' Неверно❌', reply_markup=inline_markup)
            if counter == 5:
                counter = 0
                await query.message.reply_text('Поздравляю, ты прошел тест!🎉')

            if query.data == 'go_back':
                level = 0
                counter = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)


    if level == 1:
        if spisok[-1] == 'temp':
            if query.data == 'test_temp':
                spisok.append('test_temp')
                level = 2
                await query.message.reply_text('Tecт')
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_temp[counter][0], callback_data=otvet_temp[counter][tasks_temp[counter][0]])],
                    [InlineKeyboardButton(tasks_temp[counter][1], callback_data=otvet_temp[counter][tasks_temp[counter][1]])],
                    [InlineKeyboardButton(tasks_temp[counter][2], callback_data=otvet_temp[counter][tasks_temp[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]


                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_temp[counter], reply_markup=inline_markup)
    if level == 2:
        if spisok[-1] == 'test_temp':
            if query.data == 'Verno':
                counter += 1
                await query.message.reply_text('Верно✅')
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_temp[counter][0], callback_data=otvet_temp[counter][tasks_temp[counter][0]])],
                    [InlineKeyboardButton(tasks_temp[counter][1], callback_data=otvet_temp[counter][tasks_temp[counter][1]])],
                    [InlineKeyboardButton(tasks_temp[counter][2], callback_data=otvet_temp[counter][tasks_temp[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_temp[counter], reply_markup=inline_markup)
                print(counter)

            if query.data == 'ne verno':
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton(tasks_temp[counter][0], callback_data=otvet_temp[counter][tasks_temp[counter][0]])],
                    [InlineKeyboardButton(tasks_temp[counter][1], callback_data=otvet_temp[counter][tasks_temp[counter][1]])],
                    [InlineKeyboardButton(tasks_temp[counter][2], callback_data=otvet_temp[counter][tasks_temp[counter][2]])],
                    [InlineKeyboardButton("Назад", callback_data="go_back")]
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text(question_temp[counter] + ' Неверно❌', reply_markup=inline_markup)
            if counter == 5:
                counter = 0
                await query.message.reply_text('Поздравляю, ты прошел тест!🎉')

            if query.data == 'go_back':
                level = 0
                counter = 0
                query1 = update.callback_query
                await query1.answer()
                inline_keyboard = [
                    [InlineKeyboardButton("Механика", callback_data="mechanics")],
                    [InlineKeyboardButton("Тепловые явления", callback_data="temp")],
                ]

                inline_markup = InlineKeyboardMarkup(inline_keyboard)
                await query.edit_message_text("Пожалуйста выбери что-нибудь", reply_markup=inline_markup)












async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def close_keyboard(update, context):
    await update.message.reply_text("Меню закрыто", reply_markup=ReplyKeyboardRemove())
    print(update)


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
