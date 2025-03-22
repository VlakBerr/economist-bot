import telebot
from telebot import types

import config
import data_base

bot = telebot.TeleBot(config.token)


'''
Функция start
'''
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    help_btn = types.KeyboardButton('/help')
    markup.add(help_btn)
    bot.send_message(message.chat.id, '''Привет, это Telegram-бот, который помогает пользователям управлять 
их личными финансами, включая отслеживание расходов и доходов, категоризацию финансовых операций и анализ личного бюджета.
Нажмите /help, чтобы ознакомиться со всеми командами''' )
