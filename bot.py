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


'''
Функция help
'''
@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup()

    start_btn = types.KeyboardButton('/start')
    help_btn = types.KeyboardButton('/help')

    register_btn = types.KeyboardButton('/register')
    login_btn = types.KeyboardButton('/login')
    
    add_income_btn = types.KeyboardButton('/add_income')
    add_expense_btn = types.KeyboardButton('/add_expense')

    set_goal_btn = types.KeyboardButton('/set_goal')
    view_transactions_btn = types.KeyboardButton('/view_transactions')

    statistics_btn = types.KeyboardButton('/statistics')


    markup.row(start_btn, help_btn)
    markup.row(register_btn, login_btn)
    markup.row(add_income_btn, add_expense_btn)
    markup.row(set_goal_btn, view_transactions_btn)
    markup.row(statistics_btn)

    bot.send_message(message.chat.id,
    '''
1. /start - Приветственное сообщение и краткая инструкция по использованию бота.
2. /register - Регистрация нового пользователя в системе.
3. /login - Авторизация пользователя для доступа к его данным.
4. /add_income [сумма] [категория] - Добавление дохода с указанием суммы и категории.
5. /add_expense [сумма] [категория] - Добавление расхода с указанием суммы и категории.
6. /set_goal [сумма] [описание] - Установка финансовой цели с указанием суммы и описания.
7. /view_transactions [период] - Просмотр истории транзакций за указанный период.
8. /statistics - Просмотр статистики по расходам и доходам, а также прогрессу в достижении финансовых целей.
9. /help - Список доступных команд и описание их использования.
    ''', reply_markup=markup)
