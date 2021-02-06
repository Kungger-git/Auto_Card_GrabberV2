import mysql.connector as connectSQL
import colorama


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def connect_db():
    mySQL = connectSQL.connect(
        host='localhost',
        user='root',
        password=''
    )
    myCursor = mySQL.cursor()
    
    run_once(check_database(myCursor))
    run_once(check_table(myCursor))
    myCursor.execute('USE credit_cards')
    return mySQL


def check_connection():
    if connect_db():
        print(colorama.Fore.GREEN,
            '\n[*] Connection to Database is Successful!\n',
            colorama.Style.RESET_ALL)
    else:
        print(colorama.Fore.RED,
            '\n[!!] Connection to Database is Unsuccessful\n',
            colorama.Style.RESET_ALL)


@run_once
def check_database(cursor):
    try:
        cursor.execute(
            'CREATE DATABASE IF NOT EXISTS credit_cards')
        cursor.execute('USE credit_cards')
        print(colorama.Fore.GREEN,
            '\n[*] Successfully Created Database: credit_cards', colorama.Style.RESET_ALL)
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '\n[!!] An Error has occured!', err, colorama.Style.RESET_ALL)


@run_once
def check_table(cursor):
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                `Card_Number` VARCHAR(20) NOT NULL,
                `Name` VARCHAR(50) NOT NULL,
                `Address` TEXT NOT NULL,
                `Country` VARCHAR(50) NOT NULL,
                `CVV` INT(3) NOT NULL,
                `EXP` VARCHAR(15) NOT NULL,
                PRIMARY KEY (`Card_Number`));''')
        print(colorama.Fore.GREEN,
            '\n[*] Successfully Created Table: users', colorama.Style.RESET_ALL)
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '\n[!!] An Error has occured!', err, colorama.Style.RESET_ALL)


def insertData(connection, values):
    myCursor = connection.cursor()
    sql = '''INSERT INTO
            users (Card_Number, Name, Address, Country, CVV, EXP)
            VALUES (%s,%s,%s,%s,%s,%s)'''

    val = [tuple(values)]
    try:
        myCursor.executemany(sql, val)
        myCursor.execute('SELECT * FROM users')
        myCursor.fetchall()
        connection.commit()
        print( colorama.Fore.YELLOW, myCursor.rowcount,
            'was inserted', colorama.Style.RESET_ALL)
    except connectSQL.Error as err:
        print(colorama.Fore.RED,
            '[!!] An Error has occured!', err, colorama.Style.RESET_ALL)
