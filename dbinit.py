from flask import current_app
import os
import sys

import psycopg2 as dbapi2


"""INIT_STATEMENTS = [
    "INSERT INTO USERS (EMAIL, NAME, SURNAME, PASSWORD) VALUES('salih@s.com', 'Salih', 'YILDIZ', 'asdasd')"
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()"""

DATABASE_URL = ""

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    DATABASE_URL = url


def getUsers():
    with dbapi2.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        for user in cursor:
            print(user)
        cursor.close()