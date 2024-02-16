import sqlite3
import time
import math
import re
from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addStatement(self, phone_number, title, text, author_id):
        try:
            self.__cur.execute("SELECT COUNT() as `count` FROM statements WHERE title LIKE ?", (title,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Заявление с таким id уже существует")
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO statements VALUES(NULL, ?, ?, ?, ?, ?, ?)", (phone_number, title, text, tm, author_id, 0))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False

        return True

    def getStatement(self, id):
        try:
            self.__cur.execute(f"SELECT title, text, approve FROM statements WHERE id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return False

    def getAllStatements(self):
        try:
            self.__cur.execute("SELECT * FROM statements")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return False

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД "+str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

    def getUserStatements(self, user_id):
        try:
            self.__cur.execute("""SELECT id, title, approve 
                                  FROM statements 
                                  WHERE author_id = ?""", (user_id,))
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))

        return False
    def getUserRole(self, user_id):
        try:
            self.__cur.execute(f"SELECT is_admin FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
    def updateApprove(self, statement_id, approve):
        try:
            self.__cur.execute(f"UPDATE statements SET approve = {int(approve)} WHERE id = '{int(statement_id)}'")
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
    

