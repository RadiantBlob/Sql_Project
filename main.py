import sqlite3
# from flask import Flask
# 
# app = Flask(__name__)
# 
class User:
    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

    def to_db(self):
        pass

    @classmethod
    def from_db(cls):
        connection = sqlite3.connect("poke.db") # Muss vorher angelegt werden.
        cursor = connection.cursor()
        sql = f"SELECT * "
        cursor.execute(sql)
        row = cursor.fetchone()
        connection.close()
        return User(row[0], row[1], row[2])

user = User.from_db()