import telebot
from telebot import types

import config
from data_base import Database

Database.create_table()
bot = telebot.TeleBot(config.token)

USER_ID = None


@bot.message_handler(
    func=lambda message: message.text == "Домой" or message.text == "Назад"
)
def return_to_help(message):
    bot.send_message(message.chat.id, "Вы ввели команду вернуться в функцию help")
    help(message)
    return


"""
Функция start
"""


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    help_btn = types.KeyboardButton("/help")
    markup.add(help_btn)
    bot.send_message(
        message.chat.id,
        """Привет, это Telegram-бот, который помогает пользователям управлять 
их личными финансами, включая отслеживание расходов и доходов, категоризацию финансовых операций и анализ личного бюджета.
Нажмите /help, чтобы ознакомиться со всеми командами""",
    )


"""
Функция help
"""


@bot.message_handler(commands=["help"])
def help(message):
    markup = types.ReplyKeyboardMarkup()

    start_btn = types.KeyboardButton("/start")
    help_btn = types.KeyboardButton("/help")

    register_btn = types.KeyboardButton("/register")
    login_btn = types.KeyboardButton("/login")

    add_income_btn = types.KeyboardButton("/add_income")
    add_expense_btn = types.KeyboardButton("/add_expense")

    set_goal_btn = types.KeyboardButton("/set_goal")
    view_transactions_btn = types.KeyboardButton("/view_transactions")

    statistics_btn = types.KeyboardButton("/statistics")

    markup.row(start_btn, help_btn)
    markup.row(register_btn, login_btn)
    markup.row(add_income_btn, add_expense_btn)
    markup.row(set_goal_btn, view_transactions_btn)
    markup.row(statistics_btn)

    bot.send_message(
        message.chat.id,
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
        "📜 /view_transactions — История транзакций за всё время с возможностью выбрать отдельную категорию.\n\n",
        reply_markup=markup,
        parse_mode="HTML",
    )


"""
Функция register
"""


@bot.message_handler(commands=["register"])
def register_start(message):
    markup = types.ReplyKeyboardMarkup()
    register_btn = types.KeyboardButton("/register")
    markup.add(register_btn)
    bot.send_message(
        message.chat.id, "Введите username и пароль для регистрации через пробел"
    )
    bot.register_next_step_handler(message, register_finish)


def register_finish(message):
    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    message_txt = message.text

    if message_txt.count(" ") == 1:
        username, password = message_txt.split(" ")
        if Database.register(username, password) is True:
            Database.register(username, password)
            bot.send_message(
                message.chat.id, f"Пользователь {username} успешно зарегистрирован"
            )
        else:
            bot.send_message(
                message.chat.id, "Этот username уже занят. Попробуйте ещё раз"
            )
            register_start(message)
            return
    else:
        bot.send_message(
            message.chat.id,
            "Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз",
        )
        register_start(message)
        return


"""
Функция login
"""


@bot.message_handler(commands=["login"])
def login_start(message):
    markup = types.ReplyKeyboardMarkup()
    login_btn = types.KeyboardButton("/login")
    markup.add(login_btn)
    bot.send_message(
        message.chat.id, "Введите ваш username и пароль для входа через пробел"
    )
    bot.register_next_step_handler(message, login_finish)


def login_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    message_txt = message.text

    if message_txt.count(" ") == 1:
        username, password = message_txt.split(" ")
        if Database.login(username, password) is False:
            bot.send_message(
                message.chat.id, "Неправильный username или пароль. Попробуйте ещё раз"
            )
            login_start(message)
            return
        else:
            USER_ID = Database.login(username, password)
            bot.send_message(
                message.chat.id, f"Вы успешно вошли! Здравствуйте, {username}"
            )
    else:
        bot.send_message(
            message.chat.id,
            "Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз",
        )
        login_start(message)
        return


"""
Функция set_goal
"""


@bot.message_handler(commands=["set_goal"])
def set_goal_start(message):
    global USER_ID

    markup = types.ReplyKeyboardMarkup()
    set_goal_btn = types.KeyboardButton("/set_goal")
    markup.add(set_goal_btn)

    message_to_user = "Уже имеющиеся финансовые цели:"
    goals = Database.get_all_goals(USER_ID)
    if goals is not None:
        for goal in goals:
            user_id = goal.user_id
            title = goal.title
            money_count = goal.money_count
            savings = goal.savings
            message_to_user += f"\n\nЦель: {title}, необходимо накопить: {money_count}, накоплено: {savings}"

        bot.send_message(message.chat.id, message_to_user)
    else:
        bot.send_message(message.chat.id, "У вас ещё нет финансовых целей")
    bot.send_message(
        message.chat.id,
        "Поставте финансовую цель: напишите название и цену через пробел",
    )
    bot.register_next_step_handler(message, set_goal_finish)


def set_goal_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(" ") == 1:
            title, money_count = message_txt.split(" ")
            if money_count.isdigit() is False:
                bot.send_message(
                    message.chat.id, "Вы не ввели сумму. Попробуйте ещё раз"
                )
                set_goal_start(message)
                return
            else:
                if Database.check_goal_in_table_by_id(USER_ID, title) is True:
                    Database.set_goal(USER_ID, title, money_count)
                    bot.send_message(message.chat.id, "Новая цель успешно установлена")
                else:
                    bot.send_message(
                        message.chat.id, "Такая цель уже есть. Попробуйте ещё раз"
                    )
                    set_goal_start(message)
                    return
        else:
            bot.send_message(
                message.chat.id,
                "Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз",
            )
            set_goal_start(message)
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


"""
Функция add_income
"""


@bot.message_handler(commands=["add_income"])
def add_income_start(message):
    markup = types.ReplyKeyboardMarkup()
    add_income_btn = types.KeyboardButton("/add_income")
    markup.add(add_income_btn)
    bot.send_message(
        message.chat.id, "Добавте доход с указанием категории и суммы через пробел"
    )
    bot.register_next_step_handler(message, add_income_finish)


def add_income_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(" ") == 1:
            title, income = message_txt.split(" ")
            if income.isdigit() is False:
                bot.send_message(
                    message.chat.id, "Вы не ввели сумму. Попробуйте ещё раз"
                )
                add_income_start(message)
                return
            else:
                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is True
                ):
                    price_after, save = None, None
                    price_after, save = Database.add_income(USER_ID, title, income)
                    if price_after is None or save is None:
                        bot.send_message(
                            message.chat.id,
                            f"Поздравляю! Вы накопили на свою цель!!! Вы внесли сверх {save}",
                        )
                        bot.send_message(
                            message.chat.id,
                            f'Вы желаете удалить эту цель? Напишите "Да" или "Нет"',
                        )
                        bot.register_next_step_handler(
                            message, lambda msg: add_income_delete_goal(msg, title)
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            f"Молодцы! Вы внесли уже {price_after}. Вам осталось накопить {save}",
                        )
                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is False
                ):
                    bot.send_message(
                        message.chat.id,
                        "Категория неправильно указано. Попробуйте ещё раз",
                    )
                    add_income_start(message)
                    return
        else:
            bot.send_message(
                message.chat.id,
                "Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз",
            )
            add_income_start(message)
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


def add_income_delete_goal(message, title):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        answer = message.text.strip().lower()

        if answer == "да":
            Database.delete_completed_goal(USER_ID, title)
            bot.send_message(message.chat.id, "Цель удалена")
            return
        if answer == "нет":
            bot.send_message(message.chat.id, "Хорошо, я оставлю эту финансовую цель")
            return
        else:
            bot.send_message(
                message.chat.id,
                'Вам нужно ввести только одно слово: "Да" или "Нет". Попробуйте ещё раз',
            )
            bot.register_next_step_handler(
                message, lambda msg: add_income_delete_goal(msg, title)
            )
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


"""
Функция add_expense
"""


@bot.message_handler(commands=["add_expense"])
def add_expense_start(message):
    markup = types.ReplyKeyboardMarkup()
    add_expense_btn = types.KeyboardButton("/add_expense")
    markup.add(add_expense_btn)
    bot.send_message(
        message.chat.id, "Добавте расход с указанием категории и суммы через пробел"
    )
    bot.register_next_step_handler(message, add_expense_finish)


def add_expense_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(" ") == 1:
            title, expense = message_txt.split(" ")
            if expense.isdigit() is False:
                bot.send_message(
                    message.chat.id, "Вы не ввели сумму. Попробуйте ещё раз"
                )
                add_expense_start(message)
                return
            else:
                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is True
                ):
                    price_after, save = Database.add_expense(USER_ID, title, expense)
                    if price_after > 0:
                        bot.send_message(
                            message.chat.id,
                            f"Вы уже внесли на цель {price_after} с учётом расхода. Вам осталось накопить {save}",
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            "Вы сняли больше, чем было накоплено. Я обнуляю ваш счёт",
                        )

                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is False
                ):
                    bot.send_message(
                        message.chat.id,
                        "Категория неправильно указано. Попробуйте ещё раз",
                    )
                    add_expense_start(message)
                    return

        else:
            bot.send_message(
                message.chat.id,
                "Вы допустили больше одного пробела или не поставили его. Попробуйте ещё раз",
            )
            add_expense_start(message)
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


"""
Функция view_transactions
"""


@bot.message_handler(commands=["view_transactions"])
def view_transactions_start(message):
    markup = types.ReplyKeyboardMarkup()
    view_transactions_btn = types.KeyboardButton("/view_transactions")
    markup.add(view_transactions_btn)
    bot.send_message(
        message.chat.id,
        'Введите какую-либо категорию, чтобы посмотреть по ней транзакции. Если вы хотите посмотерть транзакции за всё время, наберите "Все"!',
    )
    bot.register_next_step_handler(message, view_transactions_finish)


def view_transactions_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(" ") == 0:
            title = message_txt

            if title == "Все":
                incomes = Database.view_transactions_incomes(USER_ID, None)
                expenses = Database.view_transactions_expenses(USER_ID, None)
                if incomes is None:
                    bot.send_message(message.chat.id, f"У вас доходов нет")
                else:
                    message_to_user = "Ваши доходы:"

                    for income in incomes:
                        user_id, title, income, created_at = income
                        message_to_user += f"\n\nКатегория: {title}, внесение: {income}, время и дата: {created_at}"

                    bot.send_message(message.chat.id, message_to_user)

                if expenses is None:
                    bot.send_message(message.chat.id, f"У вас расходов нет")
                else:
                    message_to_user = "Ваши расходы:"

                    for expense in expenses:
                        user_id, title, expense, created_at = expense
                        message_to_user += f"\n\nКатегория: {title}, снятие: {expense}, время и дата: {created_at}"

                    bot.send_message(message.chat.id, message_to_user)

            else:
                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is True
                ):
                    incomes = Database.view_transactions_incomes(USER_ID, title)
                    expenses = Database.view_transactions_expenses(USER_ID, title)
                    if incomes is None:
                        bot.send_message(
                            message.chat.id, f"Доходов на эту категорию нет"
                        )
                    else:
                        message_to_user = "Ваши доходы:"

                        for income in incomes:
                            user_id, title, income, created_at = income
                            message_to_user += f"\n\nКатегория: {title}, внесение: {income}, время и дата: {created_at}"

                        bot.send_message(message.chat.id, message_to_user)

                    if expenses is None:
                        bot.send_message(
                            message.chat.id, f"Расходов на эту категорию нет"
                        )
                    else:
                        message_to_user = "Ваши расходы:"

                        for expense in expenses:
                            user_id, title, expense, created_at = expense
                            message_to_user += f"\n\nКатегория: {title}, снятие: {expense}, время и дата: {created_at}"

                        bot.send_message(message.chat.id, message_to_user)

                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is False
                ):
                    bot.send_message(
                        message.chat.id,
                        "Категория неправильно указано. Попробуйте ещё раз",
                    )
                    view_transactions_start(message)
                    return

        else:
            bot.send_message(
                message.chat.id, "Нужно ввсети только одно слово. Попробуйте ещё раз"
            )
            view_transactions_start(message)
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


"""
Функция statistics
"""


@bot.message_handler(commands=["statistics"])
def statistics_start(message):
    markup = types.ReplyKeyboardMarkup()
    statistics_btn = types.KeyboardButton("/statistics")
    markup.add(statistics_btn)
    bot.send_message(
        message.chat.id,
        'Введите какую-либо категорию, чтобы посмотреть по ней сумму ввода и вывода. Если вы хотите посмотерть сумму ввода и вывода за всё время, наберите "Все"!',
    )
    bot.register_next_step_handler(message, statistics_finish)


def statistics_finish(message):
    global USER_ID

    if message.text in ["Домой", "Назад"]:
        return_to_help(message)
        return

    if USER_ID is not None:
        message_txt = message.text

        if message_txt.count(" ") == 0:
            title = message_txt

            if title == "Все":
                incomes, expenses, path = Database.statistics(USER_ID, None)

                if incomes is None:
                    bot.send_message(message.chat.id, f"У вас доходов нет")
                else:
                    bot.send_message(message.chat.id, f"Общие внесение: {incomes}")

                if expenses is None:
                    bot.send_message(message.chat.id, f"У вас росходов нет")
                else:
                    bot.send_message(message.chat.id, f"Общие траты: {expenses}")

                photo = open("download_graficks/grafick.jpg", "rb")
                bot.send_photo(message.chat.id, photo)
                photo.close()
                Database.delete_files_in_folder(path)
            else:
                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is True
                ):
                    incomes, expenses, path = Database.statistics(USER_ID, title)

                    if incomes is None:
                        bot.send_message(
                            message.chat.id, f"У вас доходов нет на категорию {title}"
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            f"Общие внесение на категорию {title}: {incomes}",
                        )

                    if expenses is None:
                        bot.send_message(
                            message.chat.id, f"У вас росходов нет на категорию {title}"
                        )
                    else:
                        bot.send_message(
                            message.chat.id,
                            f"Общие траты на категорию {title}: {expenses}",
                        )

                    photo = open("download_graficks/grafick.jpg", "rb")
                    bot.send_photo(message.chat.id, photo)
                    photo.close()
                    Database.delete_files_in_folder(path)

                if (
                    Database.find_title_in_tables_goal_with_user_id(USER_ID, title)
                    is False
                ):
                    bot.send_message(
                        message.chat.id,
                        "Категория неправильно указано. Попробуйте ещё раз",
                    )
                    statistics_start(message)
                    return

        else:
            bot.send_message(
                message.chat.id, "Нужно ввсети только одно слово. Попробуйте ещё раз"
            )
            statistics_start(message)
            return

    else:
        bot.send_message(
            message.chat.id, "Вы не вошли в аккаунт. Войдите и попробуйте ещё раз"
        )
        login_start(message)
        return


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_message(
        message.chat.id,
        "Команда не распознана. Пожалуйста, используйте доступные кнопки или команды.",
    )
