import mysql.connector as connectSQL
import colorama

def connect_db():
    mySQL = connectSQL.connect(
        host='localhost',
        user='root',
        password='',
        database='Credit_Cards'
    )
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


def insertData(connection, values):
    myCursor = connection.cursor()
    sql = '''INSERT INTO
            Users (CardNumber, Name, Address, Country, CVV, EXP)
            VALUES (%s,%s,%s,%s,%s,%s)'''

    val = [
        (values[0], values[1], values[2], values[3], values[4], values[5])
    ]      

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