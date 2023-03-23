from os import getenv, environ
from psycopg2 import DatabaseError
from psycopg2.pool import ThreadedConnectionPool
from sys import exit
from time import sleep

__connected = False
__retries = 10 if (__retries := getenv("DB_RETRIES")) is None else int(__retries)

for i in range(__retries):
    try:
        pool = ThreadedConnectionPool(
            minconn=4,
            maxconn=16,
            host=getenv("DB_HOST"),
            database=getenv("DB_DATABASE"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            port=5432 if (port := getenv("DB_PORT")) is None else port
        )
        print("Connected to database.")
        __connected = True
        break
    except (Exception, DatabaseError) as error:
        print(f"Failed to connect to database ({i+1}/{__retries}):")
        print(error)
        sleep(5)

if not __connected:
    print(f"Failed for {__retries} retries. Set DB_RETRIES higher to increase this limit.")
    exit()