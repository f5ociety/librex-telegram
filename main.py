import telebot
from telebot import types
from urllib.parse import unquote
from tokens import BOT_TELEGRAM_TOKEN
from config import START_MESSAGE
from api import librex

bot = telebot.TeleBot(BOT_TELEGRAM_TOKEN)


def make_buttons(data):
    """
    Создание кнопок
    - спецаильного ответа
    - открытие сайта в Telegram Web App
    """
    if "special_response" in data:
        markup = types.InlineKeyboardMarkup()
        webApp = types.WebAppInfo(data["special_response"]["source"])
        markup.add(
            types.InlineKeyboardButton(
                data["special_response"]["source"], web_app=webApp
            )
        )
    else:
        markup = types.InlineKeyboardMarkup()
        # ПЕРЕВОДИМ САЙТ В HTTPS
        url: str = data["url"]
        url = url.replace("http://", "https://", 1)
        webApp = types.WebAppInfo(url)
        markup.add(types.InlineKeyboardButton(data["title"], web_app=webApp))
    return markup


def send_fast_answer(message, data):
    """Отправка спецального ответа
    Example:
    {
        "special_response": {
            "response": "Gentoo may refer to:\n\nGentoo penguin, ",
            "source": "https://wiki.femboy.hu/wiki/gentoo?lang=en"
        }
    }

    Args:
        message (json): Информация о сообщениии, отправленному боту(текст сообщения, кому отправить)
        data (json): Ответ от поисковика в виде (название, ссылка, описание)
    """

    markup = make_buttons(data)
    bot.send_message(
        message.chat.id,
        data["special_response"]["response"],
        reply_markup=markup,
    )


def send_answer(message, data):
    """Отправка обычного ответа

    Args:
        message (json): Информация о сообщениии, отправленному боту(текст сообщения, кому отправить)
        data (json): Ответ от поисковика в виде (название, ссылка, описание)
    """
    markup = make_buttons(data)
    response = f'📌 {data["title"]}\n🌐 {data["url"]}\n {data["description"]}'
    bot.send_message(
        message.chat.id,
        response,
        reply_markup=markup,
    )


def generate_answer(message, page=0):
    """Отправка запроса в поисковик

    Args:
        message (json): Информация о сообщениии, отправленному боту(текст сообщения, кому отправить)
        page (string): номер страницы поиска(по-молчанию = 0)
    """
    datas = librex.request(message.text, page)
    if datas == []:
        bot.send_message(
            message.chat.id,
            "Ничего не нашлось, попробуйте изменить запрос",
        )

    else:
        for data in datas:
            if "special_response" in data:
                send_fast_answer(message, data)
            else:
                send_answer(message, data)

        # Отправка последнего сообщения в виде кнопок навигации(1, 2, 3 и т.п.)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(f"{1}", callback_data=str(1)),
            types.InlineKeyboardButton(f"{2}", callback_data=str(2)),
            types.InlineKeyboardButton(f"{3}", callback_data=str(3)),
            types.InlineKeyboardButton(f"{4}", callback_data=str(4)),
            types.InlineKeyboardButton(f"{5}", callback_data=str(5)),
            types.InlineKeyboardButton(f"{6}", callback_data=str(6)),
            types.InlineKeyboardButton(f"{7}", callback_data=str(7)),
            types.InlineKeyboardButton(f"{8}", callback_data=str(8)),
        )
        bot.send_message(
            message.chat.id,
            message.text,
            reply_markup=markup,
        )


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, START_MESSAGE)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Захват всех запросов пользователя для генерации ответов"""
    generate_answer(message, 0)


@bot.callback_query_handler(lambda call: True)
def handle(call):
    """Функция вызывается когда выбирается номер страницы

    Args:
        call (string): Номер страницы, выбранный после поисковых ответов
    """
    generate_answer(call.message, call.data)


bot.infinity_polling()
