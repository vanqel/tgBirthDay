import datetime

from config.config import URL_DB
from typing import Any

import psycopg2

from service.utils.utils import logger


class DataBaseManager():
    def __init__(self):
        try:
            self.connection = self.get_connection()
            print("Conn succ")
            self.cursor = self.connection.cursor()

        except Exception as ex:
            print(ex)

        self.create_database()

    def querry(func):
        def wrapper(self, *args, **kwargs):
            self.connection = self.get_connection()
            result = func(self, *args, **kwargs)
            self.connection.close()
            return result

        return wrapper

    def get_connection(self):
        try:
            self.connection = psycopg2.connect(URL_DB)
            self.cursor = self.connection.cursor()
            return self.connection
        except:
            return self.connection.close()

    def execute(self, execute):
        try:
            self.cursor.execute(execute)
            self.connection.commit()
            self.connection.rollback()
            return self.cursor
        except Exception as e:
            self.connection.close()
            print(e)

    def create_database(self):
        creation = ("CREATE TABLE IF NOT EXISTS UsersTable(login text,"
                    "user_id text,name text,date date);"
                    "CREATE TABLE IF NOT EXISTS chattable(id_chat text, id_user text);"
                    "CREATE TABLE IF NOT EXISTS chats(id_chat text);")
        self.execute(creation)

    def drop(self):
        self.execute("DROP TABLE userstable")
        self.execute("DROP TABLE chattable")


    def isRegister(self, user_id):
        search = f"SELECT * FROM UsersTable WHERE user_id='{user_id}'"
        self.execute(search)
        try:
            a = self.cursor.fetchone()
            if a is None:
                return False
            else:
                return True
        except Exception as ex:
            print(ex)
            return False

    def addUser(self, login, user_id, date, name):
        insert = f"INSERT INTO UsersTable (login,user_id,name,date) VALUES ('{login}','{user_id}','{name}','{date}')"
        self.execute(insert)
        print(f"USER {name} - {user_id} ADDED IN DATABASE")

    def getDate(self, user_id: str):
        data = self.execute(f"SELECT date FROM UsersTable Where user_id = '{user_id}'").fetchone()
        return data

    def deleteuser(self, user_id):
        drop = f"DELETE FROM UsersTable WHERE user_id = '{user_id}'"
        self.execute(drop)
        print(f"USER - {user_id} DELETED")

    def linkUserChat(self, user_id, chat_id):
        insert = f"INSERT INTO chattable VALUES ('{chat_id}','{user_id}')"
        try:
            self.addChat(chat_id)
            if not self.checkUserInChat(user_id=user_id, chat_id=chat_id):
                self.execute(insert)

                print(f"USER - {user_id} ADDED IN CHAT - {chat_id}")
            else:
                print(f"USER - {user_id} ALREADY IN CHAT - {chat_id}")
        except Exception as ex:
            print(ex)
            self.connection.close()

    def delete_user_in_chat(self, user_id, chat_id):
        drop = f"DELETE FROM chattable WHERE id_user = '{user_id}' and id_chat='{chat_id}'"
        self.execute(drop)
        logger(f"USER - {user_id} DELETED IN CHAT - {chat_id}")

    def getUserInChat(self, user_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}'"
        try:
            chat = self.execute(search).fetchall()
            seq = []
            for i in chat:
                if self.getAllUsersInChat(i[0]) > 1:
                    seq += [i[0]]
            return seq
        except:
            return False

    def checkUserInChat(self, user_id, chat_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}' and id_chat='{chat_id}'"
        try:
            chat = self.execute(search).fetchall()
            return len(chat) > 0
        except:
            return False

    def addChat(self, chat_id):
        search = f"SELECT * FROM chats WHERE id_chat='{chat_id}'"
        try:
            chat = self.execute(search).fetchall()
            if not chat:
                insert = f"INSERT INTO chats VALUES ('{chat_id}')"
                self.execute(insert)
                return "CHAT ADDED"
            return 'ALREADY'
        except:
            return 'ALREADY'

    def getAllChat(self):
        search = f"SELECT id_chat FROM chats"
        data = self.execute(search).fetchall()
        return data

    def getAllUsersInChat(self,chat_id):
        users = f"SELECT * FROM chattable WHERE id_chat='{chat_id}'"
        return len(self.execute(users).fetchall())
    def getAllUsers(self):
        users = "SELECT * FROM userstable"
        return self.execute(users).fetchall()

    def getAllDate(self, chat_id) -> dict[Any] | None:
        search = f"SELECT UsersTable.user_id, UsersTable.date, UsersTable.name, UsersTable.login FROM UsersTable " \
                 f"INNER JOIN chattable ON UsersTable.user_id = chattable.id_user " \
                 f"INNER JOIN chats ON chattable.id_chat = chats.id_chat " \
                 f"WHERE chats.id_chat = '{chat_id}';"
        try:
            data = self.execute(search).fetchall()
            users = {}
            for i in data:
                users[i[0]] = {
                    'date': i[1],
                    'name': i[2],
                    'login': i[3],
                }
            return users
        except Exception as ex:
            print(ex)
            return None


    def getTargetAnivers(self, target, chat_id):

        search = f"SELECT userstable.user_id, userstable.name FROM chattable INNER JOIN userstable ON userstable.user_id = chattable.id_user " \
                 f"WHERE chattable.id_chat='{chat_id}' and (chattable.id_user <> '{target}')"
        date = f"SELECT date FROM userstable WHERE user_id='{target}'"
        try:
            list_users = self.execute(search).fetchall()
            date = self.execute(date).fetchone()
            if date[0].month > datetime.datetime.now().month and date[0].day > datetime.datetime.now().day:
                date_new = datetime.datetime(day=date[0].day, month=date[0].month, year=datetime.datetime.now().year)
            else:
                date_new = datetime.datetime(day=date[0].day, month=date[0].month, year=datetime.datetime.now().year+1)
            return [date_new, [users for users in list_users]]
        except Exception as ex:
            print(ex)


manager = DataBaseManager()
print(manager.getTargetAnivers(841244380, -1002104132939))
print(manager.getUserInChat(841244380))