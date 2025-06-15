import sqlite3
import hashlib
import matplotlib.pyplot as plt
import numpy as np
import os

from users import User, Income, Expense, Goal


class Database:
    DB='database.db'
    SCHEMA='schema.sql'

    @staticmethod
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DB, check_same_thread=False)

        cursor = connection.cursor()

        cursor.execute(sql, params)

        connection.commit()


    @staticmethod
    def select(sql, params=()):
        connection = sqlite3.connect(Database.DB)

        cursor = connection.cursor()

        cursor.execute(sql, params)
        
        raw_users=cursor.fetchall()
        users=[]
        for id, username, password in raw_users:
            user = User(id, username, password)
            users.append(user)

        return users

    @staticmethod
    def create_table():
        with open(Database.SCHEMA) as schema_file:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.executescript(schema_file.read())
            connection.commit()
            connection.close()


    @staticmethod
    def check_goal_in_table_by_id(user_id, title):
        connection = sqlite3.connect(Database.DB)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM goals WHERE user_id = ? AND title = ?', [user_id, title])
        goal = cursor.fetchall()
        if len(goal) == 0:
            return True
        else:
            return False


    @staticmethod
    def find_article_by_username(username):
        users = Database.select('SELECT * FROM users WHERE username = ?', [username])

        if not users:
            return None
        return users[0]

    @staticmethod
    def find_title_in_tables_goal_with_user_id(user_id, title):
        connection = sqlite3.connect(Database.DB)
        cursor = connection.cursor()
        cursor.execute('SELECT money_count FROM goals WHERE user_id = ? AND title = ?', [user_id, title])
        money_count = cursor.fetchall()
        if len(money_count) == 0:
            return False
        else:
            return True


    @staticmethod
    def register(username, password):
        if Database.find_article_by_username(username) is None:
            hash_password = hashlib.md5(password.encode("UTF-8")).hexdigest()
            Database.execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, hash_password])
            return True
        else:
            return False
        
    @staticmethod
    def login(username, password):
        if Database.find_article_by_username(username) is None:
            return False
        else:
            hash_password = hashlib.md5(password.encode("UTF-8")).hexdigest()
            
            connection = sqlite3.connect(Database.DB)

            cursor = connection.cursor()

            cursor.execute('SELECT password FROM users WHERE username = ?', [username])
        
            password_table = cursor.fetchone()
            password_table = password_table[0]

            if hash_password == password_table:
                cursor.execute('SELECT id FROM users WHERE username = ?', [username])
                user_id = cursor.fetchone()
                return user_id[0]
            else:
                return False

    @staticmethod
    def set_goal(user_id, title, money_count):
        Database.execute('INSERT INTO goals (user_id, title, money_count) VALUES (?, ?, ?)', 
        [user_id, title, money_count])
        return True

    @staticmethod
    def add_income(user_id, title, income):
        Database.execute('INSERT INTO incomes (user_id, title, income) VALUES (?, ?, ?)', 
        [user_id, title, income])
        
        connection = sqlite3.connect(Database.DB)
        cursor = connection.cursor()
        cursor.execute('SELECT savings FROM goals WHERE title = ?', [title])        
        price_before = int(cursor.fetchall()[0][0])
        cursor.execute('SELECT money_count FROM goals WHERE title = ?', [title])        
        money_count = int(cursor.fetchall()[0][0])

        price_after = price_before + income 
        Database.execute('UPDATE goals SET savings = ? WHERE title = ? ', [price_after, title])

        if price_after >= money_count:
            return None, price_after - money_count 
        else:
            return price_after, money_count - price_after

    @staticmethod
    def add_expense(user_id, title, expense):
        Database.execute('INSERT INTO expenses (user_id, title, expense) VALUES (?, ?, ?)', 
        [user_id, title, expense])
        
        connection = sqlite3.connect(Database.DB)
        cursor = connection.cursor()
        cursor.execute('SELECT savings FROM goals WHERE title = ?', [title])        
        price_before = int(cursor.fetchall()[0][0])
        cursor.execute('SELECT money_count FROM goals WHERE title = ?', [title])        
        money_count = int(cursor.fetchall()[0][0])

        price_after = price_before - expense 
        Database.execute('UPDATE goals SET savings = ? WHERE title = ? AND user_id = ? ', [price_after, title, user_id])

        return price_after, money_count - price_after

    @staticmethod
    def view_transactions_incomes(user_id, title):
        if title is None:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM incomes WHERE user_id = ?', [user_id])
            incomes = list(cursor.fetchall())
        else:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM incomes WHERE user_id = ? AND title = ?', [user_id, title])
            incomes = list(cursor.fetchall())

        if len(incomes) == 0:
            return None
        return incomes

    @staticmethod
    def view_transactions_expenses(user_id, title):
        if title is None:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM expenses WHERE user_id = ?', [user_id])
            expenses = list(cursor.fetchall())
        else:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM expenses WHERE user_id = ? AND title = ?', [user_id, title])
            expenses = list(cursor.fetchall())

        if len(expenses) == 0:
            return None
        return expenses

    @staticmethod
    def delete_files_in_folder(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f'Ошибка при удалении файла {file_path}. {e}')

    @staticmethod
    def statistics(user_id, title):
        if title is None:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT income FROM incomes WHERE user_id = ?', [user_id])
            incomes = list(cursor.fetchall())
            incomes_all = 0
            cursor.execute('SELECT expense FROM expenses WHERE user_id = ?', [user_id])
            expenses = list(cursor.fetchall())
            expenses_all = 0

            for i in range(len(incomes)):
                incomes_all += int(incomes[i][0])
            for i in range(len(expenses)):
                expenses_all += int(expenses[i][0])
        
        else:
            connection = sqlite3.connect(Database.DB)
            cursor = connection.cursor()
            cursor.execute('SELECT income FROM incomes WHERE user_id = ? AND title = ?', [user_id, title])
            incomes = list(cursor.fetchall())
            incomes_all = 0
            cursor.execute('SELECT expense FROM expenses WHERE user_id = ? AND title = ?', [user_id, title])
            expenses = list(cursor.fetchall())
            expenses_all = 0

            for i in range(len(incomes)):
                incomes_all += int(incomes[i][0])
            for i in range(len(expenses)):
                expenses_all += int(expenses[i][0])
            
        columns = {
        "Income": incomes_all,
        "Expense": expenses_all,
        }

        transactions = list(columns.keys())
        values = list(columns.values())

        fig, ax = plt.subplots()
        bars = ax.bar(transactions, values)

        for bar, transaction in zip(bars, transactions):
            if transaction == 'Expense':
                bar.set_color('orange')  
            else:
                bar.set_color('blue')  
        
        ax.set_title("Statistics")
        ax.set_xlabel("Incomes and Expenses")
        ax.set_ylabel("Values")

        path = "download_graficks"
        Database.delete_files_in_folder(path)
        plt.savefig("download_graficks/grafick.jpg")
        path = os.path.abspath("download_graficks/grafick.jpg")

        return incomes_all, expenses_all