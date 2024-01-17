import psycopg2


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
        self.connection = psycopg2.connect(
            "postgresql://vanqel:Q9NVdtS1pmea@ep-falling-cell-a2reg41u.eu-central-1.aws.neon.tech"
            "/telegrambot_birthday_db?sslmode=require")
        self.cursor = self.connection.cursor()
        return self.connection

    def execute(self, execute):
        try:
            self.connection = self.get_connection()
            self.cursor.execute(execute)
            self.connection.commit()
            self.connection.rollback()
        except Exception as e:
            print("Conn succ")

            print(e)

    def create_database(self):
        creation = ("CREATE TABLE UsersTable(login text,"
                    "user_id int,name text,date date);")
        self.execute(creation)

    def drop(self):
        self.execute("DROP TABLE UsersTable")

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
        insert = f"INSERT INTO userstable (login,user_id,name,date) VALUES ('{login}','{user_id}','{name}','{date}')"
        self.execute(insert)
        print(f"USER {name} - {user_id} ADDED IN DATABASE")

    def getDate(self, user_id: str):
        self.execute(f"SELECT date FROM UsersTable Where user_id = '{user_id}'")
        return self.cursor.fetchone()

    def deleteuser(self,user_id):
        drop = f"DELETE FROM public.userstable WHERE user_id = '{user_id}'"
        self.execute(drop)
        print(f"USER - {user_id} DELETED")



manager = DataBaseManager()
