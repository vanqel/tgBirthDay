import datetime
from typing import Any

import psycopg2

from config.config import URL_DB
from service.utils.utils import logger


class DataBaseManager():
    def __init__(self):
        try:
            self.connection = self.get_connection()
            self.cursor = self.connection.cursor()

        except Exception as ex:
            print(ex)

        self.create_database_tables()

    def check_connect(self):
        try:
            self.get_connection()
            logger("INFO: <b>CONNECTION SUCCEFUL</b>")
        except Exception as ex:
            logger(f"ERROR DATABASE: <b> {ex}</b>")

    def query(func):
        def wrapper(self, *args, **kwargs):
            self.connection = self.get_connection()
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    def get_connection(self):
        try:
            self.connection = psycopg2.connect(URL_DB)
            self.cursor = self.connection.cursor()
            return self.connection
        except:
            return self.connection.rollback()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except Exception as e:
            logger(f"Ошибка выполнения запроса: {e},{query}")
            self.connection.rollback()
            raise

    @query
    def create_database_tables(self):
        creation = ("CREATE TABLE IF NOT EXISTS UsersTable(login text,"
                    "user_id text,name text,date date);"
                    "CREATE TABLE IF NOT EXISTS chattable(id_chat text, id_user text);"
                    "CREATE TABLE IF NOT EXISTS chats(id_chat text);"
                    "CREATE TABLE IF NOT EXISTS userchatlink(id_user text, id_chat text, link text)")
        self.execute_query(creation)

    @query
    def drop_tables(self):
        self.execute_query("DROP TABLE userstable")
        self.execute_query("DROP TABLE chattable")

    @query
    def is_registered(self, user_id):
        search = f"SELECT * FROM UsersTable WHERE user_id='{user_id}'"
        self.execute_query(search)
        try:
            a = self.cursor.fetchone()
            if a is None:
                return False
            else:
                return True
        except Exception as ex:
            logger(ex)
            return False

    @query
    def add_user(self, login, user_id, date, name):
        insert = f"INSERT INTO UsersTable (login,user_id,name,date) VALUES (%s,%s,%s,%s)"
        params = (login, user_id, name, date)
        self.execute_query(insert, params)
        print(f"USER {name} - {user_id} ADDED IN DATABASE")

    @query
    def delete_user(self, user_id):
        drop = f"DELETE FROM UsersTable WHERE user_id = '{user_id}'"
        self.execute_query(drop)
        print(f"USER - {user_id} DELETED")

    @query
    def link_user_chat(self, user_id, chat_id):
        insert = f"INSERT INTO chattable VALUES ('{chat_id}','{user_id}')"
        try:
            self.add_chat(chat_id)
            if user_id is not None:
                if not self.check_user_in_chat(user_id=user_id, chat_id=chat_id):
                    self.execute_query(insert)

                    print(f"USER - {user_id} ADDED IN CHAT - {chat_id}")
                else:
                    print(f"USER - {user_id} ALREADY IN CHAT - {chat_id}")
        except Exception as ex:
            logger(str(ex))

    @query
    def delete_user_in_chat(self, user_id, chat_id):
        drop = f"DELETE FROM chattable WHERE id_user = '{user_id}' and id_chat='{chat_id}'"
        self.execute_query(drop)
        logger(f"USER - {user_id} DELETED IN CHAT - {chat_id}")

    @query
    def get_user_in_chat(self, user_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}'"
        try:
            chat = self.execute_query(search).fetchall()
            seq = []
            for i in chat:
                if self.get_all_users_in_chat(i[0]) > 1:
                    seq += [i[0]]
            return seq
        except:
            return False

    def check_user_in_chat(self, user_id, chat_id):
        search = f"SELECT id_chat FROM chattable WHERE id_user='{user_id}' and id_chat='{chat_id}'"
        try:
            chat = self.execute_query(search).fetchall()
            return len(chat) > 0
        except:
            return False

    def add_chat(self, chat_id):
        search = f"SELECT * FROM chats WHERE id_chat='{chat_id}'"
        try:
            chat = self.execute_query(search).fetchall()
            if not chat:
                insert = f"INSERT INTO chats VALUES ('{chat_id}')"
                self.execute_query(insert)
                return "CHAT ADDED"
            return 'ALREADY'
        except:
            return 'ALREADY'

    def delete_chat(self, chat_id):
        delete = f"DELETE FROM chats WHERE id_chat='{chat_id}'"
        self.execute_query(delete)

    @query
    def get_all_chats(self):
        search = f"SELECT id_chat FROM chats"
        data = self.execute_query(search).fetchall()
        return data

    @query
    def get_all_users_in_chat(self, chat_id):
        users = f"SELECT * FROM chattable WHERE id_chat='{chat_id}'"
        return len(self.execute_query(users).fetchall())

    @query
    def get_all_users(self):
        users = "SELECT * FROM userstable"
        return self.execute_query(users).fetchall()

    @query
    def get_all_users_date(self, chat_id) -> dict[Any] | None:
        search = f"SELECT UsersTable.user_id, UsersTable.date, UsersTable.name, UsersTable.login FROM UsersTable " \
                 f"INNER JOIN chattable ON UsersTable.user_id = chattable.id_user " \
                 f"INNER JOIN chats ON chattable.id_chat = chats.id_chat " \
                 f"WHERE chats.id_chat = '{chat_id}';"
        try:
            data = self.execute_query(search).fetchall()
            users = {}
            for i in data:
                users[i[0]] = {
                    'date': i[1],
                    'name': i[2],
                    'login': i[3],
                }
            return users
        except Exception as ex:
            logger(str(ex))
            return None

    @query
    def get_target_birthdays(self, target: str):
        '''

        :param target:
        :param chat_id:
        '''

        date = f"SELECT date FROM userstable WHERE user_id='{target}'"
        try:
            date = self.execute_query(date).fetchone()
            date_new = datetime.datetime(day=date[0].day, month=date[0].month, year=datetime.datetime.now().year)
            if date_new < datetime.datetime.now():
                date_new = datetime.datetime(day=date[0].day, month=date[0].month,year=datetime.datetime.now().year + 1)
            return date_new
        except Exception as ex:
            logger(f'get_target_birthday {ex}')
            return None

    @query
    def get_list_users_target_birthdays(self, target, chat_id):
        search = f"SELECT id_user FROM chattable " \
                 f"WHERE id_chat='{chat_id}' and (id_user <> '{target}')"
        try:
            list_users = self.execute_query(search).fetchall()
            return [user[0] for user in list_users]
        except Exception as ex:
            logger(f'get_list_users_target_birthdays {ex}')
            print(ex)
            return None

    @query
    def set_new_link(self, user_id: str, chat_id: str, link, id_new_chat):
        try:
            search = "SELECT * FROM userchatlink WHERE id_user=%s AND id_chat=%s AND link=%s"
            self.execute_query(search, (user_id, chat_id, link))
            existing_link = self.cursor.fetchone()
            if existing_link is None:
                insert = "INSERT INTO userchatlink (id_user, id_chat, link, delete_date, id_new_chat) VALUES (%s, %s, %s,%s,%s)"
                self.execute_query(insert, (
                    user_id, chat_id, link, (datetime.datetime.now() + datetime.timedelta(days=10)), id_new_chat))
                logger(f"New link set for user {user_id} in chat {chat_id}")
            else:
                logger(f"Link already exists for user {user_id} in chat {chat_id}")

        except Exception as ex:
            logger(f"{ex},setNewLink")

    @query
    def get_new_link(self, user_id, chat_id):
        try:
            uid = str(user_id)
            cid = str(chat_id)
            search = f"SELECT link, id_new_chat FROM userchatlink WHERE id_chat='{cid}' and id_user='{uid}'"
            data = self.execute_query(search).fetchone()
            return data
        except Exception as ex:
            print(ex)
            self.connection.rollback()
            return None

    @query
    def get_all_new_link(self, user_id):
        try:
            search = f"SELECT id_new_chat FROM userchatlink WHERE id_user='{user_id}'"
            lists = self.execute_query(search).fetchall()
            return [cid[0] for cid in lists]
        except Exception as ex:
            logger(f"get_all_new_link {ex}")
    @query
    def get_all_link_dates(self):
        try:
            search = f"SELECT id_new_chat, delete_date FROM userchatlink"
            return self.execute_query(search).fetchall()
        except Exception as ex:
            logger(f'getAllLinkDate {ex}')
            return []

    @query
    def delete_chat_in_user_chat_link(self, chat_id):
        try:
            delete = f"DELETE FROM userchatlink WHERE id_new_chat='{chat_id}'"
            self.execute_query(delete)
        except Exception as ex:
            logger(f"deleteChatInUserChatLink {ex}")

    @query
    def get_name(self, user_id):
        search = f"SELECT name FROM userstable WHERE user_id='{user_id}'"
        name = self.execute_query(search).fetchone()
        return name[0]

    @query
    def update_about(self, user_id, about):
        update = f"UPDATE userstable SET about = %s WHERE user_id = '%s'"
        self.execute_query(update, (about, user_id))

    @query
    def get_about(self, user_id):
        try:
            search = f"SELECT about FROM userstable WHERE user_id='{user_id}'"
            data = self.execute_query(search).fetchone()
            if self.execute_query(search).fetchone()[0] is None:
                return ""
            return data
        except Exception as ex:
            logger(f"get_about, {ex}")
            return None


database_manager = DataBaseManager()
print(database_manager.get_all_new_link(841244380))