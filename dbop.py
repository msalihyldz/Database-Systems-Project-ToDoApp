from flask import current_app
import os
import sys
import userModel
import psycopg2 as dbapi2

import account

#url = os.getenv("DATABASE_URL")

url = "postgres://pwxpfinpjbijnz:ff185279623d37be9b00ea394f348c5bf814cc9243a1f78368af3a1a1c646b47@ec2-52-31-94-195.eu-west-1.compute.amazonaws.com:5432/d3kgq0se0ml75b"

messages = {
  'insert' : 'The data is added.',
  'update' : 'The data is updated.',
  'delete' : 'The data is deleted.',
  'domains_name_key': 'Domain key should be unique, please try again.',
  'subdomains_domain_id_fkey': 'Domain has subdomains so the domain key should not deleted.',
  'users_email_key': 'You must check your credentials!',
  'error': 'Error has been occured. Please contact administrator.'
}


def checkUserMail(email):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    result = True
    user = None
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM USERS WHERE EMAIL = '{email}'""")
        resultList = cursor.fetchall()
        print(len(resultList))
        if(len(resultList) > 0):
            result = False
            user = account.User(resultList[0][0], resultList[0][1], resultList[0][2], resultList[0][3], resultList[0][4])
        connection.commit()
        cursor.close()
    return result, user

def registerUser(name, surname, email, password):
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    user = None
    try:
        with dbapi2.connect(url) as connection:
            print("register")
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO USERS(email, password, name, surname) VALUES( '{email}', '{password}', '{name}', '{surname}') RETURNING ID""")
            id_ = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return messages['insert'], id_

    except dbapi2.IntegrityError as e:
        print(e.diag.constraint_name)
        print("error: ", e.diag.message_detail)
        if e.diag.constraint_name in messages:
            return messages[e.diag.constraint_name], -1
        return messages['error'], -1
    except dbapi2.Error as e:
        print(e.pgcode)
        print("error: ", e.diag.message_detail)
        return messages['error'], -1

def getUsers():
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    result = []
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USERS")
        result = cursor.fetchall()
        cursor.close()
    return result

def getUser(uid):
    print("getuser")
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    user = None
    uid = str(uid)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            query = (f"""SELECT * FROM USERS WHERE ID = {uid} """)
            cursor.execute(query)
            resultList = cursor.fetchall()
            if(len(resultList) > 0):
                result = False
                user = account.User(resultList[0][0], resultList[0][1], resultList[0][2], resultList[0][3], resultList[0][4])
            connection.commit()
            cursor.close()
        return user
    except dbapi2.IntegrityError as e:
        print(e.diag.constraint_name)
        print("error: ", e.diag.message_detail)
        if e.diag.constraint_name in messages:
            return messages[e.diag.constraint_name], -1
        return messages['error'], -1
    except dbapi2.Error as e:
        print(e.pgcode)
        print("error: ", e.diag.message_detail)
        return messages['error'], -1

