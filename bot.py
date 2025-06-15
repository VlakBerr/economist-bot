import telebot
from telebot import types

import config
from data_base import Database

Database.create_table()
bot = telebot.TeleBot(config.token)

USER_ID = None

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
    "<b>Основные команды:</b>\n"
    "🔹 /start — Приветственное сообщение и краткая инструкция по использованию бота.\n"
    "🔹 /register — Регистрация нового пользователя в системе.\n"
    "🔹 /login — Авторизация пользователя для доступа к его данным.\n"
    "🔹 /help - Список доступных команд и описание их использования.\n\n"
    "<b>Финансовые операции:</b>\n"
    "➕ /add_income [категория] [сумма] — Добавить доход с указанием суммы и категории.\n"
    "➖ /add_expense [категория] [сумма] — Добавить расход с указанием суммы и категории.\n\n"
    "<b>Цели и анализ:</b>\n"
    "🎯 /set_goal [описание] [сумма] — Установить финансовую цель.\n"
    "📊 /statistics — Просмотр статистики по доходам, расходам и прогрессу целей.\n"
    "📜 /view_transactions — История транзакций за всё время с возможностью выбрать отдельную категорию.\n\n"
, reply_markup=markup, parse_mode="HTML")


'''
Функция register
'''
@bot.message_handler(commands=['register'])
def register_start(message):
    markup = types.ReplyKeyboardMarkup()
    register_btn = types.KeyboardButton('/register')
    markup.add(register_btn)
    bot.send_message(message.chat.id,'Введите username и пароль для регистрации через пробел')
    bot.register_next_step_handler(message, register_finish)
    
def register_finish(message):
    message_txt = message.text
    
    if message_txt.count(' ') == 1:
        username, password = message_txt.split(' ')
        if Database.register(username, password) is True:
            Database.register(username, password)
            bot.send_message(message.chat.id, f'Пользователь {username} успешно зарегистрирован')
        else:
            bot.send_message(message.chat.id,'Этот username уже занят. Попробуйте ещё раз')
            bot.register_next_step_handler(message, register_start)

    else:
        bot.send_message(message.chat.id,'Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз')
        bot.register_next_step_handler(message, register_start)

'''
Функция login
'''
@bot.message_handler(commands=['login'])
def login_start(message):
    markup = types.ReplyKeyboardMarkup()
    login_btn = types.KeyboardButton('/login')
    markup.add(login_btn)
    bot.send_message(message.chat.id,'Введите ваш username и пароль для входа через пробел')
    bot.register_next_step_handler(message, login_finish)
    
def login_finish(message):
    global USER_ID

    message_txt = message.text
    
    if message_txt.count(' ') == 1:
        username, password = message_txt.split(' ')
        if Database.login(username, password) is False:
            bot.send_message(message.chat.id,'Неправильный username или пароль. Попробуйте ещё раз')
            bot.register_next_step_handler(message, login_start)
        else:
            USER_ID = Database.login(username, password)
            bot.send_message(message.chat.id,f'Вы успешно вошли! Здравствуйте, {username}')
    else:
        bot.send_message(message.chat.id,'Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)

'''
Функция set_goal
'''
@bot.message_handler(commands=['set_goal'])
def set_goal_start(message):
    markup = types.ReplyKeyboardMarkup()
    set_goal_btn = types.KeyboardButton('/set_goal')
    markup.add(set_goal_btn)
    bot.send_message(message.chat.id,'Поставте финансовую цель: напишите название и цену через пробел')
    bot.register_next_step_handler(message, set_goal_finish)
    
def set_goal_finish(message):
    global USER_ID
    
    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(' ') == 1:
            title, money_count = message_txt.split(' ')
            if money_count.isdigit() is False:
                bot.send_message(message.chat.id,'Вы не ввели сумму. Попробуйте ещё раз')
                bot.register_next_step_handler(message, set_goal_start)
            else:
                if Database.check_goal_in_table_by_id(USER_ID, title) is True:
                    Database.set_goal(USER_ID, title, money_count)
                    bot.send_message(message.chat.id,'Новая цель успешно установлена')
                else:
                    bot.send_message(message.chat.id,'Такая цель уже есть. Попробуйте ещё раз')
                    bot.register_next_step_handler(message, set_goal_start)
        else:
            bot.send_message(message.chat.id,'Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз')
            bot.register_next_step_handler(message, set_goal_start)

    else:
        bot.send_message(message.chat.id,'Вы не вошли в аккаунт. Войдите и попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)

'''
Функция add_income
'''
@bot.message_handler(commands=['add_income'])
def add_income_start(message):
    markup = types.ReplyKeyboardMarkup()
    add_income_btn = types.KeyboardButton('/add_income')
    markup.add(add_income_btn)
    bot.send_message(message.chat.id,'Добавте доход с указанием категории и суммы через пробел')
    bot.register_next_step_handler(message, add_income_finish)
    
def add_income_finish(message):
    global USER_ID
    
    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(' ') == 1:
            title, income = message_txt.split(' ')
            if income.isdigit() is False:
                bot.send_message(message.chat.id,'Вы не ввели сумму. Попробуйте ещё раз')
                bot.register_next_step_handler(message, add_income_start)
            else:
                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is True:
                    price_after, save = None, None
                    price_after, save = Database.add_income(USER_ID, title, int(income))
                    if price_after is None or save is None:
                        bot.send_message(message.chat.id,f'Поздравляю! Вы накопили на свою цель!!! Вы внесли сверх {save}')
                    else:
                        bot.send_message(message.chat.id,f'Молодцы! Вы внесли уже {price_after}. Вам осталось накопить {save}')

                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is False:
                    bot.send_message(message.chat.id,'Категория неправильно указано. Попробуйте ещё раз')
                    bot.register_next_step_handler(message, add_income_start)

        else:
            bot.send_message(message.chat.id,'Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз')
            bot.register_next_step_handler(message, add_income_start)

    else:
        bot.send_message(message.chat.id,'Вы не вошли в аккаунт. Войдите и попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)

'''
Функция add_expense
'''
@bot.message_handler(commands=['add_expense'])
def add_expense_start(message):
    markup = types.ReplyKeyboardMarkup()
    add_expense_btn = types.KeyboardButton('/add_expense')
    markup.add(add_expense_btn)
    bot.send_message(message.chat.id,'Добавте расход с указанием категории и суммы через пробел')
    bot.register_next_step_handler(message, add_expense_finish)
    
def add_expense_finish(message):
    global USER_ID
    
    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(' ') == 1:
            title, expense = message_txt.split(' ')
            if expense.isdigit() is False:
                bot.send_message(message.chat.id,'Вы не ввели сумму. Попробуйте ещё раз')
                bot.register_next_step_handler(message, add_expense_start)
        
            if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is True:
                price_after, save = Database.add_expense(USER_ID, title, int(expense))
                bot.send_message(message.chat.id,f'Вы уже внесли на цель {price_after} с учётом расхода. Вам осталось накопить {save}')

            if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is False:
                bot.send_message(message.chat.id,'Категория неправильно указано. Попробуйте ещё раз')
                bot.register_next_step_handler(message, add_expense_start)
        
        else:
            bot.send_message(message.chat.id,'Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз')
            bot.register_next_step_handler(message, add_expense_start)

    else:
        bot.send_message(message.chat.id,'Вы не вошли в аккаунт. Войдите и попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)

'''
Функция view_transactions
'''
@bot.message_handler(commands=['view_transactions'])
def view_transactions_start(message):
    markup = types.ReplyKeyboardMarkup()
    view_transactions_btn = types.KeyboardButton('/view_transactions')
    markup.add(view_transactions_btn)
    bot.send_message(message.chat.id,'Введите какую-либо категорию, стобы посмотреть по ней транзакции. Если вы хотите посмотерть транзакции за всё время, наберите "Все"!')
    bot.register_next_step_handler(message, view_transactions_finish)
    
def view_transactions_finish(message):
    global USER_ID
    
    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(' ') == 0:
            title = message_txt
            
            if title == 'Все':
                incomes = Database.view_transactions_incomes(USER_ID, None)
                expenses = Database.view_transactions_expenses(USER_ID, None)
                if incomes is None:
                    bot.send_message(message.chat.id, f'У вас доходов нет')
                else:
                    for income in incomes:
                        user_id, title, income, created_at = income
                        bot.send_message(message.chat.id, f'ДОХОД: название: {title}, внесение: {income}, время и дата: {created_at}')
                
                if expenses is None:
                    bot.send_message(message.chat.id, f'У вас росходов нет')
                else:
                    for expense in expenses:
                        user_id, title, expense, created_at = expense
                        bot.send_message(message.chat.id, f'Расход: название: {title}, снятие: {expense}, время и дата: {created_at}')    
            else:
                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is True:
                    incomes = Database.view_transactions_incomes(USER_ID, title)
                    expenses = Database.view_transactions_expenses(USER_ID, title)
                    if incomes is None:
                        bot.send_message(message.chat.id, f'Доходов на эту категорию нет')
                    else:
                        for income in incomes:
                            user_id, title, income, created_at = income
                            bot.send_message(message.chat.id, f'ДОХОД: название: {title}, внесение: {income}, время и дата: {created_at}')

                    if expenses is None:
                        bot.send_message(message.chat.id, f'Расходов на эту категорию нет')
                    else:
                        for expense in expenses:
                            user_id, title, expense, created_at = expense
                            bot.send_message(message.chat.id, f'Расход: название: {title}, снятие: {expense}, время и дата: {created_at}')    

                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is False:
                    bot.send_message(message.chat.id,'Категория неправильно указано. Попробуйте ещё раз')
                    bot.register_next_step_handler(message, view_transactions_start)
        
        else:
            bot.send_message(message.chat.id,'Нужно ввсети только одно слово. Попробуйте ещё раз')
            bot.register_next_step_handler(message, view_transactions_start)

    else:
        bot.send_message(message.chat.id,'Вы не вошли в аккаунт. Войдите и попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)

'''
Функция statistics
'''
@bot.message_handler(commands=['statistics'])
def statistics_start(message):
    markup = types.ReplyKeyboardMarkup()
    statistics_btn = types.KeyboardButton('/statistics')
    markup.add(statistics_btn)
    bot.send_message(message.chat.id,'...')
    bot.register_next_step_handler(message, statistics_finish)
    
def statistics_finish(message):
    global USER_ID
    
    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(' ') == 0:
            title = message_txt
            
            if title == 'Все':
                incomes, expenses = Database.statistics(USER_ID, None)

                if incomes is None:
                    bot.send_message(message.chat.id, f'У вас доходов нет')
                else:
                    bot.send_message(message.chat.id, f'Общие внесение: {incomes}')
                
                if expenses is None:
                    bot.send_message(message.chat.id, f'У вас росходов нет')
                else:
                   bot.send_message(message.chat.id, f'Общие траты: {expenses}')

                with open("download_graficks/grafick.jpg", 'rb') as photo:
                    bot.send_photo(message.chat.id, photo)
                
            else:
                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is True:
                    incomes, expenses = Database.statistics(USER_ID, title)

                    if incomes is None:
                        bot.send_message(message.chat.id, f'У вас доходов нет на категорию {title}')
                    else:
                        bot.send_message(message.chat.id, f'Общие внесение на категорию {title}: {incomes}')

                    if expenses is None:
                        bot.send_message(message.chat.id, f'У вас росходов нет на категорию {title}')
                    else:
                        bot.send_message(message.chat.id, f'Общие траты на категорию {title}: {expenses}')

                    with open("download_graficks/grafick.jpg", 'rb') as photo:
                        bot.send_photo(message.chat.id, photo)

                if Database.find_title_in_tables_goal_with_user_id(USER_ID, title) is False:
                    bot.send_message(message.chat.id,'Категория неправильно указано. Попробуйте ещё раз')
                    bot.register_next_step_handler(message, statistics_start)

        else:
            bot.send_message(message.chat.id,'Нужно ввсети только одно слово. Попробуйте ещё раз')
            bot.register_next_step_handler(message, statistics_start)

    else:
        bot.send_message(message.chat.id,'Вы не вошли в аккаунт. Войдите и попробуйте ещё раз')
        bot.register_next_step_handler(message, login_start)
