import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class Database(object):
    connection = None,

    def connect(self):
        load_dotenv()

        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )

    def get_users(self):
        cursor = self.connection.cursor(prepared=True)
        query_string = (""" SELECT `bgg_id`, `username` FROM users """)
        cursor.execute(query_string)

        results = []
        rows = cursor.fetchall()

        for row in rows:
            # See: https://stackoverflow.com/a/60172473/1686528
            results.append(dict(zip(cursor.column_names, row)))

        cursor.close()

        return results

    def get_user(self, user: str):
        cursor = self.connection.cursor(prepared=True)
        query_string = (""" SELECT `bgg_id`, `username` FROM users WHERE username = '{}' """).format(user)
        cursor.execute(query_string)

        results = []
        rows = cursor.fetchall()

        for row in rows:
            # See: https://stackoverflow.com/a/60172473/1686528
            results.append(dict(zip(cursor.column_names, row)))

        cursor.close()

        return results

    def create_user(self, user: dict):
        cursor = self.connection.cursor(prepared=True)

        try:
            query = ("""INSERT INTO users (`bgg_id`, `username`) VALUES (%s, %s)""")
            cursor.execute(query, (user['id'], user['username']))
            self.connection.commit()

        except Error as error:
            return False
        finally:
            cursor.close()
            return True

    def disconnect(self):
        self.connection.close()
