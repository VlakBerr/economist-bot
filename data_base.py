import sqlite3
import hashlib


from users import User


class Database:
    DB='database.db'
    SCHEMA='schema.sql'

    @staticmethod
    def execute(sql, params=()):
        connection = sqlite3.connect(Database.DB)

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
    def find_article_by_username(id):
        users = Database.select('SELECT * FROM users WHERE id = ?', [id])

        if not users:
            return None
        return users[0]
