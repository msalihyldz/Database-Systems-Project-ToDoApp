from flask import current_app
import os
import sys
import psycopg2 as dbapi2
from datetime import datetime
from flask_login import current_user

import account

#url = os.getenv("DATABASE_URL")

url = "postgres://pwxpfinpjbijnz:ff185279623d37be9b00ea394f348c5bf814cc9243a1f78368af3a1a1c646b47@ec2-52-31-94-195.eu-west-1.compute.amazonaws.com:5432/d3kgq0se0ml75b"

messages = {
  'insert' : 'The data is added.',
  'update' : 'The data is updated.',
  'delete' : 'The data is deleted.',
  'error': 'Error has been occured. Please contact administrator.'
}

JOINS = {
    'wsData' : 'SELECT WS.ID, MODIFYDATE, WS.TITLE as ws_title, WS.COLOR as ws_color, WS.DESCRIPTION as ws_description, ws.LISTORDER as ws_order, COUNT(distinct ACCS), count(distinct TSK) FROM workspaces WS LEFT JOIN useraccess ACCS ON WS.id = ACCS.workspaceid LEFT JOIN LIST LST ON WS.id = LST.workspaceid LEFT JOIN TASK TSK ON TSK.listid = LST.id WHERE ws.id = %s GROUP BY WS.ID;',
    'taskAndUser' : 'SELECT tsk.id AS id,tsk.content AS task_content,tsk.listid AS list_id,tsk.assignedid AS assignedid,tsk.deadline AS end_date,tsk.isdone AS done,tsk.importance AS tsk_importance,tsk.listorder AS list_order,tsk.donedate AS tsk_donedate,usr.name AS user_name,usr.surname AS user_surname FROM task tsk LEFT JOIN users usr ON usr.id=tsk.assignedid WHERE listid=%s ORDER BY listorder',
    'wsUserList' : 'SELECT usr.id AS id, usr.name AS user_name, usr.surname AS user_surname, usraccss.workspaceid AS ws_id FROM useraccess usraccss JOIN users usr ON usr.id = usraccss.userid WHERE workspaceid = %s',
    'commentData' : 'SELECT c.id AS c_id,c.userid AS c_userid,c.taskid AS c_taskid,c.content AS c_content,c.modifydate AS c_modifydate,u.name AS u_name,u.surname AS u_surname FROM comments c LEFT JOIN users u on c.userid=u.id WHERE taskid = %s',
    'userStats' : 'SELECT * FROM (SELECT COUNT(DISTINCT U2) AS WS_COUNT FROM users u JOIN useraccess u2 on u.id=u2.userid WHERE u.id= %s ) w_count,(SELECT COUNT(DISTINCT T) AS TASK_COUNT FROM users u JOIN task t on u.id=t.assignedid WHERE u.id= %s ) t_count',
    'numberofDoneTasks' : 'SELECT COUNT(DISTINCT T),U.name AS USER_NAME,U.surname AS uSER_SURNAME FROM task T LEFT JOIN list l on l.id=T.listid iNNER JOIN users u on u.id=T.assignedid WHERE workspaceid = %s AND T.isdone GROUP BY U.id',
    'workspaceData' : 'SELECT WS.id,title,color,description FROM workspaces WS LEFT JOIN useraccess u ON WS.id=u.workspaceid WHERE U.userid = %s'
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
    now = datetime.now()
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO USERS(email, password, name, surname, registerdate) VALUES( '{email}', '{password}', '{name}', '{surname}', '{now}') RETURNING ID""")
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

def createWorkspace(title, description, color, order):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    dt = datetime.now()
    print('title', title)
    print('description', description)
    print('color', color)
    print('order', order)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO WORKSPACES(modifydate, title, description, color, listorder) VALUES( '{dt}', '{title}', '{description}', '{color}', '{order}') RETURNING ID""")
            id_ = cursor.fetchone()[0]
            cursor.execute(f"""INSERT INTO USERACCESS(userid, workspaceid, isowner) VALUES( '{current_user.uid}', '{id_}', '{True}') RETURNING ID""")
            connection.commit()
            print(id_)
            cursor.close()
        return id_
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

def getUserWorkspaces(uid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM USERACCESS WHERE USERID = '{uid}'""")
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def getWorkspaceData(wsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['wsData'],(str(wsId),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

"""def getUserTasks(wsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        print(wsId)
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['wsToTask'],(str(wsId),))
            result = cursor.fetchall()
            print(result)
            connection.commit()
            cursor.close()
        return result
    except dbapi2.IntegrityError as e:
        print(e.diag.constraint_name)
        print("error: ", e.diag.message_detail)
        if e.diag.constraint_name in messages:
            return messages[e.diag.constraint_name], -1
        return messages['error'], -1
    except dbapi2.Error as e:
        print(e.pgcode)
        print("error: ", e.diag.message_detail)
        return messages['error'], -1"""

def getWsLists(wsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""SELECT * FROM LIST WHERE WORKSPACEID = '{wsId}'""")
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def getListTasks(lsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['taskAndUser'],(str(lsId),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def getTaskComments(tId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['commentData'],(str(tId),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def getWorkspaceUsers(wid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['wsUserList'],(str(wid),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def addTask(content, listId, assignedId, endDate, importance, listorder):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    endDate = datetime.strptime(endDate,f"""%d/%m/%Y""")
    if assignedId == "None":
        assignedId = None
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            if assignedId != None:
                cursor.execute(f"""INSERT INTO TASK(content, listid, assignedid, deadline, isdone, importance, listorder) VALUES( '{content}', '{listId}', '{assignedId}', '{endDate}', '{False}', '{importance}', '{listorder}') RETURNING ID""")
            else:
                print('girdi')
                cursor.execute(f"""INSERT INTO TASK(content, listid, assignedid, deadline, isdone, importance, listorder) VALUES( '{content}', '{listId}', NULL, '{endDate}', '{False}', '{importance}', '{listorder}') RETURNING ID""")
            print(cursor.query)
            id_ = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return id_
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

def updateTask(taskId, content, listId, assignedId, endDate, isDone, importance, listorder):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    endDate = datetime.strptime(endDate,f"""%d/%m/%Y""")
    if assignedId == "None":
        assignedId = None
    if(isDone):
        isDone = 1
        donedate = datetime.now()
    else: 
        isDone = 0
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            if assignedId != None:
                if isDone:
                    query = f"""UPDATE TASK SET content = '{content}', listid = '{listId}', assignedid = '{assignedId}', deadline = '{endDate}', isDone = '{True}', importance = '{importance}', listorder = '{listorder}', donedate = '{donedate}' WHERE id = '{taskId}' """
                else:
                    query = f"""UPDATE TASK SET content = '{content}', listid = '{listId}', assignedid = '{assignedId}', deadline = '{endDate}', isDone = '{False}' WHERE id = '{taskId}' """
            else:
                if isDone:
                    query = f"""UPDATE TASK SET content = '{content}', listid = '{listId}', assignedid = NULL, deadline = '{endDate}', isDone = '{True}', importance = '{importance}', listorder = '{listorder}', donedate = '{donedate}' WHERE id = '{taskId}' """
                else:
                    query = f"""UPDATE TASK SET content = '{content}', listid = '{listId}', assignedid = NULL, deadline = '{endDate}', isDone = '{False}' WHERE id = '{taskId}' """
            cursor.execute(query)
            res = cursor.rowcount
            connection.commit()
            cursor.close()
        return res
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

def addList(title, wid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO LIST(title, workspaceid, createdBy) VALUES( '{title}', '{wid}', '{current_user.uid}') RETURNING ID""")
            print(cursor.query)
            id_ = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return id_
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

def addFriend(userId, wid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            print(f"""INSERT INTO USERACCESS(userid, workspaceid, isowner) VALUES( '{userId}', '{wid}', '{False}') RETURNING ID""")
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO USERACCESS(userid, workspaceid, isowner) VALUES( '{userId}', '{wid}', '{False}') RETURNING ID""")
            id_ = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return id_
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

def addComment(content, taskId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    now = datetime.now()
    try:
        with dbapi2.connect(url) as connection:
            print(f"""INSERT INTO COMMENTS(userid, taskid, content, modifydate) VALUES( '{current_user.uid}', '{taskId}', '{content}', '{now}') RETURNING ID""")
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO COMMENTS(userid, taskid, content, modifydate) VALUES( '{current_user.uid}', '{taskId}', '{content}', '{now}') RETURNING ID""")
            id_ = cursor.fetchone()[0]
            connection.commit()
            cursor.close()
        return id_
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

def deleteTask(taskId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    now = datetime.now()
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""DELETE FROM TASK WHERE id = '{taskId}'""")
            connection.commit()
            cursor.close()
        return True
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

def updateWorkspace(wsId, title, description, color, order):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            query = f"""UPDATE WORKSPACES SET title = '{title}', description = '{description}', color = '{color}', listorder = '{order}' WHERE id = '{wsId}' """
            cursor.execute(query)
            res = cursor.rowcount
            connection.commit()
            cursor.close()
        return res
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

def deleteWorkspace(wsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    now = datetime.now()
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""DELETE FROM WORKSPACES WHERE id = '{wsId}'""")
            connection.commit()
            cursor.close()
        return True
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

def userStats(uid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    user = None
    uid = str(uid)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['userStats'],(str(uid),str(uid),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def updateUserPassword(newPassword):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            query = f"""UPDATE USERS SET password = '{newPassword}' WHERE id = '{current_user.uid}' """
            cursor.execute(query)
            res = cursor.rowcount
            connection.commit()
            cursor.close()
        return res
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

def updateUser(uid, name, surname):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            print('sa')
            cursor = connection.cursor()
            query = f"""UPDATE USERS SET name = '{name}', surname = '{surname}' WHERE id = '{current_user.uid}' """
            cursor.execute(query)
            res = cursor.rowcount
            connection.commit()
            cursor.close()
        return res
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

def deleteUser():
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    now = datetime.now()
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""DELETE FROM USERS WHERE id = '{current_user.uid}'""")
            connection.commit()
            cursor.close()
        return True
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

def workspaceStats(wsId):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['numberofDoneTasks'],(str(wsId),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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

def getUserWorkspacesData(uid):
    #url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    try:
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(JOINS['workspaceData'],(str(uid),))
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
        return result
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