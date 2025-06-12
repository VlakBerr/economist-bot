import sqlite3
import hashlib


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
    def find_article_by_username(username):
        users = Database.select('SELECT * FROM users WHERE username = ?', [username])

        if not users:
            return None
        return users[0]

    @staticmethod
    def find_title_in_tables_with_name_USERNAME(title_table, title):
        title = Database.select(f'SELECT * FROM {title_table} WHERE title = ?', [title])

        if title is None:
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

    #@staticmethod
    #def login(username, password):
    #    if Database.find_article_by_username(username) is None:
    #        return False
    #    else:
    #        hash_password = hashlib.md5(password.encode("UTF-8")).hexdigest()
    #        user = Database.select('SELECT * FROM users WHERE username = ?', [username])
    #        password_table = user[0][2]
    #        if hash_password == password_table:
    #            return user[0]
    #        else:
    #            return False

        
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

    #@staticmethod
    #def set_goal(title_table, price, title):
    #    Database.execute(f'''
    #    CREATE TABLE IF NOT EXISTS {title_table}(
    #    title TEXT NOT NULL UNIQUE,
    #    price TEXT NOT NULL,
    #    savings TEXT NOT NULL DEFAULT '0'
    #    )''',[])
    #    Database.execute(f'INSERT INTO {title_table} (title, price) VALUES (?, ?)', [title, price])
    #    return True
#
    #@staticmethod
    #def add_income(title_table, title, income):
    #    connection = sqlite3.connect(Database.DB)
    #    cursor = connection.cursor()
    #    cursor.execute(f'SELECT savings FROM {title_table} WHERE title = ?', [title])        
    #    price_before = int(cursor.fetchall()[0][0])
    #    cursor.execute(f'SELECT price FROM {title_table} WHERE title = ?', [title])        
    #    goal_price = int(cursor.fetchall()[0][0])
#
    #    price_after = price_before + income 
    #    Database.execute(f'''
    #    UPDATE {title_table} SET savings = ? WHERE title = ? ''', [price_after, title])
#
    #    if price_after >= goal_price:
    #        return None, price_after - goal_price 
    #    else:
    #        return price_after, goal_price - price_after
#
    #@staticmethod
    #def add_expense(title_table, title, income):
    #    connection = sqlite3.connect(Database.DB)
    #    cursor = connection.cursor()
    #    cursor.execute(f'SELECT savings FROM {title_table} WHERE title = ?', [title])        
    #    price_before = int(cursor.fetchall()[0][0])
    #    cursor.execute(f'SELECT price FROM {title_table} WHERE title = ?', [title])        
    #    goal_price = int(cursor.fetchall()[0][0])
#
    #    price_after = price_before - income 
    #    Database.execute(f'''
    #    UPDATE {title_table} SET savings = ? WHERE title = ? ''', [price_after, title])
#
    #    return price_after, goal_price - price_after

    @staticmethod
    def set_goal(user_id, title, money_count):
        Database.execute('INSERT INTO goals (user_id, title, money_count) VALUES (?, ?, ?)', 
        [user_id, title, money_count])
        return True
