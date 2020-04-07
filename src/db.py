import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class Database(object):
    """
    Class for handling database interactions.

    @TODO Specific queries need to move on out of here.
    """
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

        row = cursor.fetchone()

        # See: https://stackoverflow.com/a/60172473/1686528
        user = dict(zip(cursor.column_names, row))
        cursor.close()

        return user

    def create_user(self, user: dict):
        """
        Add a new user to the database table.
        """
        cursor = self.connection.cursor(prepared=True)

        try:
            query = """INSERT INTO users (`bgg_id`, `username`) VALUES (%s, %s)"""
            cursor.execute(query, (user['id'], user['username']))
            self.connection.commit()

        except Error as error:
            return False
        finally:
            cursor.close()
            return True

    def get_games(self):
        cursor = self.connection.cursor(prepared=True)
        query_string = """ SELECT * FROM games """
        cursor.execute(query_string)

        results = []
        rows = cursor.fetchall()

        for row in rows:
            # Modified from https://stackoverflow.com/a/60172473/1686528 to return a list of titles instead of dict.
            game = dict(zip(cursor.column_names, row))
            results.append(game['title'])

        cursor.close()

        return results

    def create_game(self, game):
        """
        Add a game to the database.
        """
        cursor = self.connection.cursor(prepared=True)

        try:
            query_string = ("""
                INSERT IGNORE INTO games (`bgg_id`, `title`)
                VALUES (%s, %s)
            """)
            cursor.execute(
                query_string,
                (game['@objectid'], game['name']['#text'])
            )
            self.connection.commit()
        except Error as error:
            return False
        finally:
            cursor.close()
            return True

    def get_user_collection(self, username: str):
        """
        Get the games for a selected user.
        :param username:
        :return:
        """
        cursor = self.connection.cursor(prepared=True)
        query_string = ("""
        SELECT `title` FROM games
        WHERE id IN (
            SELECT `game_id` FROM user_collection
            WHERE `user_id` = (
                SELECT id FROM users WHERE username = '{}'
            )
        )
        """).format(username)
        cursor.execute(query_string)

        results = []
        rows = cursor.fetchall()

        for row in rows:
            # See: https://stackoverflow.com/a/60172473/1686528
            results.append(dict(zip(cursor.column_names, row)))

        cursor.close()

        return results

    def add_game_to_collection(self, game, user):
        """
        Insert a game into a user's collection.
        """
        cursor = self.connection.cursor(prepared=True)

        try:
            query_string = """
                INSERT IGNORE INTO user_collection (`user_id`, `game_id`)
                VALUES (
                    (
                        SELECT id FROM users
                        WHERE bgg_id = %s
                        LIMIT 1
                    ),
                    (
                        SELECT id FROM games
                        WHERE bgg_id = %s
                        LIMIT 1                    
                    )
                )
            """
            cursor.execute(
                query_string,
                (user['id'], game['@objectid'])
            )
            self.connection.commit()
        except Error as error:
            return False
        finally:
            cursor.close()
            return True
