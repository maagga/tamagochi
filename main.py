import random

import telebot
from telebot import types
from trend import trend, trendm, pogoda, ssulca1, ssulca2 

API_TOKEN = '6099493407:AAGRj2u4X9fS4c4mj_6dCwlOkwfdecRMvQU'

bot = telebot.TeleBot(API_TOKEN)


def get_random_link(num,links_collection):
    for index, value in enumerate(pogoda):
        if num in value:
            _index = index
            break
    links = links_collection[_index]
    return random.choice(links)


class User:
    def __init__(self, chat_id, gender):
        self.chat_id = chat_id
        self.gender = gender


USERS = {}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('Woman', callback_data='woman')
    item1 = types.InlineKeyboardButton('Man', callback_data='man')
    markup.add(item, item1)
    bot.reply_to(message, "Привіт я Тамагочі Бот! Я можу тобі допомогти підібрати одяг за погодою")

    bot.send_message(message.chat.id, 'Вибери потрібний тобі варіант', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'woman':
            USERS[call.message.chat.id] = User(call.message.chat.id, call.data)
            bot.send_message(call.message.chat.id, 'Напиши скільки в тебе зараз градусів від 0 до 30 С ?'
                                                   '(Підбор трендів може зайняти деякий час')
        if call.data == 'man':
            USERS[call.message.chat.id] = User(call.message.chat.id, call.data)
            bot.send_message(call.message.chat.id, 'Напиши скільки в тебе зараз градусів від 0 до 30 С ?'
                                                   '(Підбор трендів може зайняти деякий час')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if trend.get(message.text):
        user = USERS.get(message.chat.id)
        if user and user.gender == 'woman':
            bot.send_message(message.chat.id, trend.get(message.text).format(get_random_link(int(message.text), ssulca1)))
        if user and user.gender == 'man':
            bot.send_message(message.chat.id, trendm.get(message.text).format(get_random_link(int(message.text), ssulca2)))


bot.infinity_polling()

