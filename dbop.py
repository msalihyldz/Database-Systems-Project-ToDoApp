from flask import current_app
import os
import sys
import userModel
import psycopg2 as dbapi2

url = os.getenv("DATABASE_URL")




def checkUserMail(email):
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    result = True
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USERS WHERE EMAIL == %s", (email,))
        if(len(cursor.fetchall()) > 0):
            result = False
        cursor.close()
    return result


def registerUser(name, surname, email, password):
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
      with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO USERS(EMAIL, NAME, SURNAME, PASSWORD) VALUES( %s, %s, %s, %s)", (email, name, surname, password))
        id_ = cursor.fetchone()[0]
        return messages['insert'], id_

    except dbapi2.IntegrityError as e:
      print(e.diag.constraint_name)
      print("dance ", e.diag.message_detail)
      if e.diag.constraint_name in messages:
        return messages[e.diag.constraint_name], -1
      return messages['error'], -1
    except dbapi2.Error as e:
      print(e.pgcode)
      print("mance: ", e.diag.message_detail)
      return messages['error'], -1
    