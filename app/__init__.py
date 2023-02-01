from flask import Flask

app = Flask(__name__)
from app import views
import sqlite3


conn = sqlite3.connect('app/static/data/database.db')
cur = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS utilisateur(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT, password TEXT, email TEXT, spots_id TEXT)""")
conn.execute("""CREATE TABLE IF NOT EXISTS spots(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, spot_name TEXT, location TEXT, denivele INTEGER, debit INTEGER)""")

if cur.execute("SELECT * FROM utilisateur WHERE id=1").fetchone() == None:
    req = "insert into utilisateur(id, username, password, email, spots_id) values ('1', 'admin', 'admin', 'admin@gmail.com', '')"
    cur.execute(req)
elif cur.execute("SELECT * FROM spots WHERE id=1").fetchone() == None:
    print("1")
    req = "insert into spots(id, spot_name, location, denivele, debit) values ('1', 'La Seille', 'Jura', '200', '7')"
    cur.execute(req)
elif cur.execute("SELECT * FROM spots WHERE id=2").fetchone() == None:
    print("2")
    req = "insert into spots(id, spot_name, location, denivele, debit) values ('2', 'JO base for 2024', 'Vaires-Sur-Marne', '20', '14')"
    cur.execute(req)
elif cur.execute("SELECT * FROM spots WHERE id=3").fetchone() == None:
    print("3")
    req = "insert into spots(id, spot_name, location, denivele, debit) values ('3', 'Sault-Brenaz', 'Sault-Brenaz', '10', '9')"
    cur.execute(req)

conn.commit()
conn.close()
