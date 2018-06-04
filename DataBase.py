import mysql.connector
from flask import Flask

DataBase = Flask(__name__)

def saveToDatabase():
    conn = mysql.connector.connect(host="127.0.0.1",
                                   user="owe8_pg4",
                                   db="owe8_pg4",
                                   passwd="blaat1234")
    cursor = conn.cursor()
    cursor.execute("""select * from Woorden """)
    bla = cursor.fetchall()
    cursor.close()
    conn.close()
    return str(bla)

@DataBase.route('/')
def main():
    return saveToDatabase()



