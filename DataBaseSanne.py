import mysql.connector
from flask import Flask
DataBase = Flask(__name__)

def saveToDatabase(edges, words):

    conn = mysql.connector.connect(host="85.214.90.171",
                                   user="owe8_pg4",
                                   db="owe8_pg4",
                                   passwd="blaat1234")
    cursor = conn.cursor()

    term = words.keys()
    type = words.values()

    for i in edges:
        i = i.split(" ")
        woordenID = i[0]
        woorden_woordenID = i[1]

    for j in edges.values():
        similarity = j[0]
        del j[0]

    for k in edges.values():
        pubID = k

    sql_command = """
    INSERT INTO Woord (Term, type)
    VALUE (term, type); 
    """

    cursor.execute(sql_command)

    conn.commit()

    cursor.close()
    conn.close()
    return str('hellooooooooo')

#@DataBase.route('/')
#def main():
#    return saveToDatabase()

if __name__ == '__saveToDatabase__':
    DataBase.run()
