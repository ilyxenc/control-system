import sqlite3
import datetime
from Crypto.Hash import SHA256

# служебные ответы
accessed = 'ACCESSED'
accessDenied = 'ACCESS DENIED'

# типы доступа:
admin = "admin"
user = "user"

# местоположение БД
dbPath = "control/database.db"

# подключение / создание БД
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# создание таблицы пользователей
def createTableUsersWithDefault(login = 'admin', password = '12345678', userType = 'admin'):
    sql = '''CREATE TABLE IF NOT EXISTS users(login text, password text, access_type text, UNIQUE(login));'''
    cursor.execute(sql)
    conn.commit()
    try:
        sql = '''INSERT INTO users(login, password, access_type) VALUES(?, ?, ?);'''
        # пользователь по умолчанию ('admin', '12345678')
        values = (login, password, userType)
        cursor.execute(sql, values)
        conn.commit()
    except:
        pass

# создание нового пользователя
def insertUser(username, password, access_type = "user"):
    values = (username, password, access_type)
    sql = '''INSERT INTO users(login, password, access_type) VALUES(?,?,?);'''
    cursor.execute(sql, values)
    conn.commit()
    print('\nUser `' + username + '` added successfully\n')

# проверка доступа
def isThereAUserOrNot(username, password):
    values = (username, password)
    sql = '''SELECT * FROM users WHERE login = ? AND password = ?;'''
    cursor.execute(sql, values)
    conn.commit()
    data = cursor.fetchall()
    if len(data) == 1 and data[0][0] == values[0]and data[0][1] == values[1]:
        return(accessed, data[0][2])
    else:
        return(accessDenied, 0)

# создание таблицы проверки целостности
def createTableData():
    sql = '''CREATE TABLE IF NOT EXISTS data(path text, hash text, time text, UNIQUE(hash));'''
    cursor.execute(sql)
    conn.commit()

# добавление файла
def insertFile(path):
    time = str(datetime.datetime.now())

    with open(path, mode='rb') as file: # b is important -> binary
            content = file.read()

    h = str(SHA256.new(content).hexdigest())
    values = (path, h, time)
    sql = '''INSERT INTO data(path, hash, time) VALUES(?,?,?);'''
    try:
        cursor.execute(sql, values)
        conn.commit()
        print('\nData from `' + path + '` added successfully\n')
    except:
        print('\nIS ALREADY EXISTS IN DB\n')

# проверка доступа
def checkFile(path):
    try:
        with open(path, mode='rb') as file: # b is important -> binary
            content = file.read()

        h = str(SHA256.new(content).hexdigest())
        values = (path, h)

        sql = '''SELECT * FROM data WHERE path = ? AND hash = ?;'''
        cursor.execute(sql, values)
        conn.commit()
        data = cursor.fetchall()
        if len(data) == 1 and data[0][0] == values[0]and data[0][1] == values[1]:
            return(True, data[0][2])
        else:
            return(False, 'File is not in the table')
    except:
        return(False, 'No file')

