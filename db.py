import psycopg2
import psycopg2.extras
from functions import hash_pwd
import os
import ipdb


def _is_connected(func):

    def wrapper(self, *args, **kwargs):
        if self.cursor.closed is True:
            # print("Connecting.")
            self.connect()
        else:
            # print("Already connected.")
            pass
        result = func(self, *args, **kwargs)
        self.conn.commit()
        return result

    return wrapper

class Database():
    database_name = os.environ['DATABASE_NAME']

    def __init__(self, tableName):
        self.username = os.environ["DATABASE_USER"] 
        self.password = os.environ["DATABASE_PASSWORD"]
        self.host = os.environ["DATABASE_HOST"]
        self.tableName = tableName
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(host=self.host,
                                     database=self.database_name,
                                     user=self.username,
                                     password=self.password)
        self.cursor = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        return self.cursor

    def closeConnection(self):
        self.conn.commit()
        self.conn.close()

    @_is_connected
    def view_all(self):
        query = f"select * from {self.tableName};"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    @_is_connected
    def view_query(self, query, values=()):
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result

    @_is_connected
    def view_where(self, where: tuple):
        query = f"select * from {self.tableName} where {where[0]}=%s;"
        self.cursor.execute(query, (where[1], ))
        result = self.cursor.fetchall()
        return result

class Users(Database):
    """
    CREATE TABLE "users" (
	"id" SERIAL,
	"username" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	PRIMARY KEY ("id","username")
);
    """
    def __init__(self):
        tableName = "users"
        super().__init__(tableName)

    @_is_connected
    def add_user(self, username, password):
        query = f"INSERT INTO {self.tableName} (username, password) VALUES (%s, %s);"
        self.cursor.execute(query, (username, password))

    @_is_connected
    def get_hash(self, username):
        query = f"SELECT password FROM {self.tableName} WHERE username=%s;"
        res = self.view_query(query, (username,))
        try:
            return res[0][0]
        except:
            return None

    @_is_connected
    def get_user_id(self, username):
        query = f"SELECT id FROM {self.tableName} WHERE username=%s;"
        res = self.view_query(query, (username,))
        try:
            return res[0][0]
        except:
            return None

class Attachments(Database):
    """
    CREATE TABLE "attachments" (
	"id" SERIAL,
	"chat_id" INT NOT NULL,
	"content" TEXT NOT NULL,
	PRIMARY KEY ("id")
);
    """
    def __init__(self):
        tableName = "attachments"
        super().__init__(tableName)

    @_is_connected
    def add_attachment(self, chat_id, content):
        query = f"INSERT INTO {self.tableName} (chat_id, content) VALUES (%s, %s);"
        self.cursor.execute(query, (chat_id, content))

    @_is_connected
    def get_content(self, idd):
        query = f"SELECT password FROM {self.tableName} WHERE id=%s;"
        res = self.view_query(query, (idd,))
        try:
            return res
        except:
            return None

class Chats(Database):
    """
    CREATE TABLE "chats" (
    "chat_id" SERIAL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
    """
    def __init__(self):
        tableName = "chats"
        super().__init__(tableName)

    @_is_connected
    def add_chat(self, user_id):
        query = f"INSERT INTO {self.tableName} (user_id) VALUES (%s);"
        self.cursor.execute(query, (user_id, ))

    @_is_connected
    def get_chats(self, user_id, limit=10):
        query = f"SELECT chat_id FROM {self.tableName} WHERE user_id=%s ORDER BY chat_id DESC LIMIT %s;;"
        res = self.view_query(query, (user_id, limit))
        res = [i[0] for i in res]
        try:
            return res
        except:
            return None

    @_is_connected
    def get_last_chat(self, user_id):
        query = f"SELECT chat_id FROM {self.tableName} WHERE user_id=%s ORDER BY chat_id DESC LIMIT 1;"
        res = self.view_query(query, (user_id,))
        try:
            return res[0][0]
        except:
            return None

class Messages(Database):
    """
    CREATE TABLE "messages" (
    "message_id" SERIAL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "user_id" INT NOT NULL,
    "chat_id" INT NOT NULL,
    "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
    """
    def __init__(self):
        tableName = "messages"
        super().__init__(tableName)

    @_is_connected
    def add_message(self, content, user_id, chat_id):
        query = f"INSERT INTO {self.tableName} (content, user_id, chat_id) VALUES (%s, %s, %s);"
        self.cursor.execute(query, (content, user_id, chat_id))

    @_is_connected
    def get_messages(self, chat_id):
        query = f"SELECT user_id, content FROM {self.tableName} WHERE chat_id=%s;"
        res = self.view_query(query, (chat_id,))
        try:
            return res
        except:
            return None

# users = Users()
#
# pwdd = hash_pwd("nav")
# print(pwdd)
# users.insert("u1", pwdd)
# msg = Messages()
# ipdb.set_trace()
# from functions import convert_to_history
# msgs = msg.get_messages(8)
# print(convert_to_history([]))
