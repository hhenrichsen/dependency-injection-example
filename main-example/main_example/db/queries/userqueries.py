from uuid import UUID

from db import Connection
from db.models.user import User
from services.password.password import PasswordService
from util.valid import validate_param


class UserQueries:
    def __init__(
        self,
        connection: Connection,
        hasher: PasswordService
    ):
        self.__connection = connection
        self.__hasher = hasher

    def create_user(
        self, username: str, email: str, raw_password: str, display_name: str
    ):
        validate_param('username', username, str)
        validate_param('email', email, str)
        validate_param('raw_password', raw_password, str)
        validate_param('display_name', display_name, str)

        hashed_password = self.__hasher.hash(raw_password)

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO users(username, email, password, display_name) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id, username, display_name, email;
                """,
                (username, email, hashed_password, display_name),
            )

            for row in cursor:
                return User(*row)
            return None

    def get_user_by_id(self, id: UUID | str) -> User | None:
        validate_param('id', id, [str, UUID])

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, display_name, email 
                FROM users 
                WHERE active=true AND id=(%s);
                """,
                (str(id),),
            )

            for row in cursor:
                return User(*row)
            return None

    def get_user_by_username(self, username: str) -> User | None:
        validate_param('username', username, str)

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, display_name, email 
                FROM users 
                WHERE active=true AND username=(%s);
                """,
                (username,),
            )

            for row in cursor:
                return User(*row)
            return None

    def get_user_by_email(self, email: str) -> User | None:
        validate_param('email', email, str)

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, display_name, email 
                FROM users 
                WHERE active=true AND email=(%s);
                """,
                (email,),
            )

            for row in cursor:
                return User(*row)
            return None

    def get_user_by_email_and_password(self, email: str, password: str) -> User | None:
        validate_param('email', email, str)
        validate_param('password', password, str)

        with self.__connection.pool.getconn() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, display_name, email, password 
                FROM users 
                WHERE active=true AND email=(%s);
                """,
                (email,),
            )

            for row in cursor:
                passwd = row[-1]
                if not self.__hasher.valid(password, passwd) or passwd is None:
                    return None
                else:
                    # Exclude password from user data
                    return User(*row[:-1])
            return None
