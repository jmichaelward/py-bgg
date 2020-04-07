import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class Database(object):
    connection = None,

    def connect(self):
        """
        Connect to the database.
        """
        load_dotenv()

        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )

    def disconnect(self):
        """
        Disconnect from the database.
        """
        self.connection.close()

    def get_users(self):
        """
        Get all users from the database.
        """
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
        """
        Get a single user from the database.
        """
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
        """
        Add a new user to the database table.
        """
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
