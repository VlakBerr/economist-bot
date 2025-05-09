import sqlite3
import hashlib


from users import User


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
            Database.execute(schema_file.read())

    @staticmethod
    def find_article_by_username(username):
        users = Database.select('SELECT * FROM users WHERE username = ?', [username])

        if not users:
            return None
        return users[0]

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