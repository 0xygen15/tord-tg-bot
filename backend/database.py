import psycopg2
import pickle

import logging

from data.config import DB_HOST, DB_PORT, DB_USERNAME, DB_PWD, DB_NAME
from backend.users import Users

logging.basicConfig(level=logging.INFO)

class Database:
    @classmethod
    def create_database_if_not_exists(cls):
        try:
            connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PWD, host=DB_HOST, port=DB_PORT)
            connection.autocommit = True
            cursor = connection.cursor()

            cursor.execute(""" CREATE database main """)
            logging.info("Database 'main' has been successfuly created!")

            connection.commit()
            connection.close()
        except psycopg2.errors.DuplicateDatabase:
            logging.info("Database 'main' already exists, therefore create-script skipped.")
        else:
            cls.create_users_table()


    @classmethod
    def create_users_table(cls):
        connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME, port=DB_PORT)
        cursor = connection.cursor()

        query = """
            CREATE TABLE IF NOT EXISTS users (
            user_id TEXT UNIQUE,
            lang_code TEXT,
            tord_game BYTEA,
            nie_game BYTEA,
            chat_id TEXT,
            chat_type TEXT,
            username TEXT,
            fName TEXT,
            lName TEXT
            ) 
            """

        cursor.execute(query)
        logging.info("Table 'users' was successfully created in database 'ctd'!")

        connection.commit()
        connection.close()

    @classmethod
    def add_user_to_db(cls, users_obj: Users):
        user_id = users_obj.user_id
        lang_code = users_obj.lang_code

        tord_game = pickle.dumps(users_obj.tord_game)
        nie_game = pickle.dumps(users_obj.nie_game)

        chat_id = users_obj.chat_id
        chat_type = users_obj.chat_type
        username = users_obj.username
        fName = users_obj.fName
        lName = users_obj.lName

        connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME,
                                      port=DB_PORT)
        logging.info(f"[INFO] Method {cls.add_user_to_db.__name__} connected to database {DB_NAME}.")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = '%s'", (user_id,))
        logging.debug(f"[INFO] Method {cls.add_user_to_db.__name__} has executed SELECT query.")
        result = cursor.fetchone()
        logging.info(f"[INFO] Method {cls.add_user_to_db.__name__}: result fetched")
        if result is None:
            query = """
                    INSERT INTO users (user_id, lang_code, tord_game, nie_game, 
                                        chat_id, chat_type, 
                                        username, fName, lName) 
                                        VALUES ('%s', %s, %s, %s, '%s', %s, %s, %s, %s)
                    """
            data = (user_id, lang_code, tord_game, nie_game,
                    chat_id, chat_type,
                    username, fName, lName)
            cursor.execute(query, data)
            logging.info(f"Method {cls.add_user_to_db.__name__} has executed INSERT query.")


        connection.commit()
        connection.close()

    @classmethod
    def get_user_obj_from_db(cls, the_user_id: str | int) -> Users:
        connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME, port=DB_PORT)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE user_id = '%s'"
        cursor.execute(query, (the_user_id,))
        data = cursor.fetchall()
        logging.info(f"This data fetched while getting user obj from db {data}")
        x = data[0]

        return_obj = Users(x[0],
                           x[1],
                           pickle.loads(x[2]),
                           pickle.loads(x[3]),
                           x[4],
                           x[5],
                           x[6],
                           x[7],
                           x[8],)

        connection.commit()
        connection.close()

        return return_obj



    @classmethod
    def update_user_obj(cls, the_user_id, new_obj):
        user_id = new_obj.user_id
        lang_code = new_obj.lang_code

        tord_game = pickle.dumps(new_obj.tord_game)
        nie_game = pickle.dumps(new_obj.nie_game)

        chat_id = new_obj.chat_id
        chat_type = new_obj.chat_type
        username = new_obj.username
        fName = new_obj.fName
        lName = new_obj.lName

        try:
            connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME, port=DB_PORT)
            cursor = connection.cursor()

            query = """UPDATE users SET user_id = %s, lang_code = %s, tord_game = %s, nie_game = %s, 
                chat_id = %s, chat_type = %s, 
                username = %s, fName = %s, lName = %s
                WHERE user_id = %s"""

            cursor.execute(query, (str(user_id), lang_code, tord_game, nie_game,
                                   str(chat_id), chat_type,
                                   username, fName, lName,
                                   str(the_user_id),))
        except Exception as e:
            logging.info(f"Error fetching user data: {e}")

        finally:
            connection.commit()
            connection.close()

    @classmethod
    def get_user_lang_code(cls, user_id):
        try:
            connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME,port=DB_PORT)
            cursor = connection.cursor()

            query = """SELECT lang_code FROM USERS WHERE user_id = '%s'"""
            cursor.execute(query, (user_id,))
            lang_code = cursor.fetchone()[0]
            return str(lang_code)

        except Exception as e:
            logging.info(f"Error fetching user data: {e}")
        finally:
            connection.commit()
            connection.close()


    @classmethod
    def change_user_lang_code(cls, lang_code, user_id):
        try:
            connection = psycopg2.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PWD, database=DB_NAME, port=DB_PORT)
            cursor = connection.cursor()

            query = "UPDATE users SET lang_code = %s WHERE user_id = '%s'"
            data = (lang_code, user_id)
            cursor.execute(query, data)
        except Exception as e:
            logging.info(f"Error fetching user data: {e}")
        finally:
            connection.commit()
            connection.close()
