import os
import sys

import psycopg2 as dbapi2


def getUsers():
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        for user in cursor:
            print(user)
        cursor.close()