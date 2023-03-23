from os import getenv, environ
from psycopg2 import DatabaseError
from psycopg2.pool import ThreadedConnectionPool
from sys import exit
from time import sleep


class Connection:
    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        port: int = 5432,
        retries: int = 10,
        min_conn: int = 4,
        max_conn: int = 16,
    ):
        self.__connected = False
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self.__port = port
        self.__retries = retries
        self.__min_conn = min_conn
        self.__max_conn = max_conn
        self.pool = None

    def connect(self):
        for i in range(self.__retries):
            try:
                self.pool = ThreadedConnectionPool(
                    host=self.__host,
                    database=self.__database,
                    user=self.__user,
                    password=self.__password,
                    port=self.__port,
                    minconn=self.__min_conn,
                    maxconn=self.__max_conn,
                )
                print("Connected to database.")
                self.__connected = True
                break
            except (Exception, DatabaseError) as error:
                print(f"Failed to connect to database ({i+1}/{self.__retries}):")
                print(error)
                sleep(5)

        if not self.__connected:
            print(
                f"Failed for {self.__retries} retries. Set DB_RETRIES higher to increase this limit."
            )
            return None
