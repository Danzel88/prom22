import os
import sqlite3
from sqlite3 import IntegrityError

from tgbot.config import load_config

config = load_config(".env")


class Database:
    CREATE_REVIEW_TABLE = '''CREATE TABLE review(
        id INTEGER PRIMARY KEY,
        tg_id INTEGER TYPE UNIQUE,
        username VARCHAR(100),
        role VARCHAR(10),
        personal_info VARCHAR(255),
        review TEXT);
    '''
    CREATE_CHAT_MESSAGES = '''CREATE TABLE chat_msg(
        id INTEGER PRIMARY KEY,
        tg_id INTEGER TYPE UNIQUE,
        username VARCHAR(100),
        name VARCHAR(100),
        grade VARCHAR(5),
        school VARCHAR(100),
        message VARCHAR(201));
    '''
    CREATE_STICKERPACK_TABLE = '''CREATE TABLE stickerpack(
        id INTEGER PRIMARY KEY,
        tg_id INTEGER TYPE UNIQUE,
        username VARCHAR(100),
        phrase TEXT);
    '''
    CREATE_USER_LIST = '''CREATE TABLE all_users(
        id INTEGER PRIMARY KEY,
        tg_id INTEGER TYPE UNIQUE,
        username VARCHAR(100));
    '''

    TABLES = [CREATE_REVIEW_TABLE, CREATE_CHAT_MESSAGES,
              CREATE_STICKERPACK_TABLE, CREATE_USER_LIST]

    def __init__(self, name=None):
        self.name = name
        self._conn = self.connection()

    def _execute_query(self, query, val):
        cursor = self._conn.cursor()
        try:
            cursor.execute(query, val)
        except IntegrityError:
            print("Уже есть запись")
            return False
        self._conn.commit()
        cursor.close()
        return True

    def create_db(self):
        """Создаем базу"""
        connection = sqlite3.connect(self.name)
        cursor = connection.cursor()
        self.create_tables(self.TABLES, cursor)
        cursor.close()

    @staticmethod
    def create_tables(tables_name, cursor):
        for table in tables_name:
            cursor.execute(table)

    def connection(self):
        """Конектимся к БД. Если БД нет - создаем её"""
        database_path = os.path.join(os.getcwd(), self.name)
        if not os.path.exists(database_path):
            self.create_db()
        return sqlite3.connect(self.name)

    def create_user(self, data):
        insert_query = '''INSERT INTO all_users (tg_id, username) values (?,?)'''
        return self._execute_query(insert_query, (data['tg_id'], data['username']))

    def crete_review(self, data):
        insert_query = '''INSERT INTO review (tg_id, username, role, personal_info, review) 
                values (?,?,?,?,?)'''
        return self._execute_query(insert_query, (data['tg_id'], data['username'],
                                                  data["role"], data["pers_info"],
                                                  data['review']))

    def create_msg_to_all(self, data):
        insert_query = '''INSERT INTO chat_msg (tg_id, username, name, grade, 
        school, message) values (?,?,?,?,?,?)'''
        return self._execute_query(insert_query, (data["tg_id"], data["username"], data["name"],
                                   data["grade"],data["school"], data["text"]))


database = Database(config.db.database)
