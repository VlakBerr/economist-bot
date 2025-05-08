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
