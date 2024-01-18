from config.conifg import URL_DB
from typing import List, Any

import psycopg2


# Когда нибудь перепишу на sqlalhemy

class DataBaseManager():
    def __init__(self):
        try:
            self.connection = self.get_connection()
            print("Conn succ")
            self.cursor = self.connection.cursor()

        except Exception as ex:
            print(ex)

        self.create_database()

    def get_connection(self):
        self.connection = psycopg2.connect(URL_DB)
        self.cursor = self.connection.cursor()
        return self.connection

    def execute(self, execute):
        try:
            self.connection = self.get_connection()
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
                    "CREATE TABLE IF NOT EXISTS chats(id_chat text)")
        self.execute(creation)

    def drop(self):
        try:
            self.execute("DROP TABLE userstable")
            self.execute("DROP TABLE chattable")
        finally:
            self.connection.close()

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
        finally:
            self.connection.close()

    def addUser(self, login, user_id, date, name):
        insert = f"INSERT INTO UsersTable (login,user_id,name,date) VALUES ('{login}','{user_id}','{name}','{date}')"
        self.execute(insert)
        self.connection.close()
        print(f"USER {name} - {user_id} ADDED IN DATABASE")

    def getDate(self, user_id: str):
        data = self.execute(f"SELECT date FROM UsersTable Where user_id = '{user_id}'").fetchone()
        self.connection.close()
        return data

    def deleteuser(self, user_id):
        drop = f"DELETE FROM UsersTable WHERE user_id = '{user_id}'"
        self.execute(drop)
        self.connection.close()
        print(f"USER - {user_id} DELETED")

    def linkUserChat(self, user_id, chat_id):
        insert = f"INSERT INTO chattable VALUES ('{chat_id}','{user_id}')"
        try:
            self.addChat(chat_id)
            if not self.checkUserInChat(user_id=user_id, chat_id=chat_id):
                self.execute(insert)
                self.connection.close()
                print(f"USER - {user_id} ADDED IN CHAT - {chat_id}")
            else:
                print(f"USER - {user_id} ALREADY IN CHAT - {chat_id}")
            self.connection.close()
        except Exception as ex:
            print(ex)
            self.connection.close()

    def delete_user_in_chat(self, user_id, chat_id):
        drop = f"DELETE FROM chattable WHERE id_user = '{user_id}' and id_chat='{chat_id}'"
        self.execute(drop)
        self.connection.close()
        print(f"USER - {user_id} DELETED IN CHAT - {chat_id}")

    def getUserInChat(self, user_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}'"
        try:
            chat = self.execute(search).fetchall()
            return [x[0] for x in chat]
        except:
            return False
        finally:
            self.connection.close()

    def checkUserInChat(self, user_id, chat_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}' and id_chat='{chat_id}'"
        try:
            chat = self.execute(search).fetchall()
            return len(chat) > 0
        except:
            return False
        finally:
            self.connection.close()

    def addChat(self, chat_id):
        search = f"SELECT * FROM chats WHERE id_chat='{chat_id}'"
        try:
            chat = self.execute(search).fetchall()
            if not chat:
                insert = f"INSERT INTO chats VALUES ('{chat_id}')"
                self.execute(insert)
                self.connection.close()
                return "CHAT ADDED"
            return 'ALREADY'
        except:
            return 'ALREADY'
        finally:
            self.connection.close()

    def getAllChat(self):
        search = f"SELECT id_chat FROM chats"
        data = self.execute(search).fetchall()
        self.connection.close()
        return data

    def getAllDate(self, chat_id) -> dict[Any]:
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


manager = DataBaseManager()
manager.getAllDate(-1002104132939)
