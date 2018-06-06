import mysql.connector
from flask import Flask

DataBase = Flask(__name__)

#maakt connectie met de database en haalt data op m.b.v query's
def loadFromDatabase():
    conn = mysql.connector.connect(host="127.0.0.1",
                                   user="owe8_pg4",
                                   db="owe8_pg4",
                                   passwd="blaat1234")
    cursor = conn.cursor()

    cursor.execute("""select Woorden.Woorden_ID, Woord.term from Woorden inner join Woord on Woorden.Woorden_ID = Woord.Woord_ID""")
    links1 = cursor.fetchall()
    cursor.execute("""select Woorden.Woorden_Woorden_ID, Woord.term, Woorden.Similarity, Waarnemingen.Artikel_Artikel_ID from Woorden inner join Waarnemingen on Woorden.edge_ID = Waarnemingen.Edge_ID inner join Woord on Woorden.Woorden_Woorden_ID = Woord.Woord_ID""")
    links2 = cursor.fetchall()
    cursor.execute("""select Waarnemingen.Edge_ID, Waarnemingen.Artikel_Artikel_ID from Waarnemingen""")
    Waarn_edge = cursor.fetchall()
    cursor.close()
    conn.close()
    for waarneming in Waarn_edge:
	Waarndict(zip(waarneming[0], waarneming[1])
	 
    return str(Waarndict)

@DataBase.route('/')
def main():
    try:
        return loadFromDatabase()
    except Exception as e:
        return e

if __name__ == '__main__':
    DataBase.run()

