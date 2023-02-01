from app import app
from flask import render_template
from flask import request, redirect
from flask_swagger_ui import get_swaggerui_blueprint

import sqlite3
import json
import os

user_spot = {'name': "", 'password': "", 'spots_fait': ""}
user = {'name': "", 'password': "", 'id_spot': ""}

@app.route('/static/<path:path>')
def send_tatic(path):
  return send_from_directory('static', path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': 'projet'
  }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

"""
def userdata2():
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  data = cur.execute("SELECT * FROM utilisateur").fetchall()
  return data
"""

def spotsdata():
  document_path = os.getcwd() + '/app/static/data/spots.json'
  f = open(document_path, 'r')
  data = json.load(f)
  f.close()
  return data

def spotsdata2():
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  data = cur.execute("SELECT * FROM spots").fetchall()
  return data



def regularisation_id():
    conn = sqlite3.connect('app/static/data/database.db')
    cur = conn.cursor()

    cur.execute("SELECT MAX(id) FROM spots")
    max_id = cur.fetchone()[0]

    cur.execute("SELECT id FROM spots ORDER BY id")
    ids = [row[0] for row in cur.fetchall()]
    for i, id in enumerate(ids, 1):
        if id != i:
            cur.execute("UPDATE spots SET id=? WHERE id=?", (i, id))
            conn.commit()

    conn.close()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')

@app.post('/login')
def login():
  global user
  global user_spot
  password = request.form.get('passwordd', default='*', type=str)
  name = request.form.get('username', default='*', type=str)


  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  data = cur.execute("SELECT password, spots_id FROM utilisateur WHERE username = ?", (name,)).fetchone()
  if data == None:
    return index()
  elif password != data[0]:
    return index()
  else:
    pass

  spotname = []
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  spots = data[1].split()
  for i in spots:
    spotname.append(cur.execute("SELECT spot_name FROM spots WHERE id=?",(i)).fetchone())

  conn.close()
  user_spot = {'name': name, 'password': password, 'spots_fait': spotname}
  user = {'name': name, 'password': password, 'id_spot': data[1]}
  
  return redirect('show')

@app.post('/signupverif')
def signupverif():
  global user, user_spot
  user ={}
  user_spot = {}
  password = request.form.get('passwordd', default='*', type=str)
  name = request.form.get('username', default='*', type=str)
  email = request.form.get('email', default='*', type=str)
  spotss = ""

  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()

  req = "insert into utilisateur( username, password, email, spots_id) values (?, ?, ?, ?)"
  cur.execute(req, (name, password, email, spotss))
  conn.commit()
  conn.close()



  user_spot = {'name': name, 'spots_fait': spotss}
  user = {'name': name, 'id_spot': None}

  return params()

@app.route('/show')
def params():
  global user
  global user_spot

  name = user_spot['name']
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  data = cur.execute("SELECT spots_id FROM utilisateur WHERE username=?",(name,)).fetchone()
  conn.close()

  spotname = []
  denivele = []
  debit = []
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  for i in data[0]:
    if i == " ":
      pass
    else:
      spotname.append(cur.execute("SELECT spot_name FROM spots WHERE id=?", (i,)).fetchone())
      debit.append(cur.execute("SELECT debit FROM spots WHERE id=?", (i,)).fetchone())
      denivele.append(cur.execute("SELECT denivele FROM spots WHERE id=?", (i,)).fetchone())


  conn.close()

  user_spot1 = {'name': name, 'spots_fait': spotname,'denivele': denivele,'debit': debit}

  return render_template('show.html', utilisateur=user_spot1)


@app.route('/ajout')
def ajout():
  global user, user_spot

  total = []

  regularisation_id()

  data = spotsdata2()
  for i in data:
    id = i[0]
    spot_name = i[1]
    location = i[2]
    denivele = i[3]
    debit = i[4]
    spot_info = "L\'id est : " + str(id) + " Le nom du spot est : " + str(spot_name) + " Sa localisation est : " + str(location) + " Le dénivelé est de : " + str(denivele) + " Le débit lui est de : " + str(debit) + "       "
    total.append(spot_info)

  name = user_spot['name']
  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  data2 = cur.execute("SELECT spots_id FROM utilisateur WHERE username=?",(name,)).fetchone()
  conn.close()

  spots_fait = user['id_spot']



  return render_template('ajout.html', infos=total, spots=spots_fait, d=len(data))

@app.post('/ajouter')
def ajouter():
  global user, user_spot

  les = []
  fait = []

  data = len(spotsdata2())
  for i in range(data):
    spot = "spot_" + str(i+1)
    if request.form.get(spot) == "on":
      fait += str(i+1)

  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()

  latype = user['name']
  tout = ' '.join(fait)
  req = "UPDATE utilisateur SET spots_id = ? WHERE username = ?"
  cur.execute(req, (tout, latype))
  conn.commit()
  conn.close()

  data_spots = spotsdata2()
  for y in data_spots:
    id_spots = y[0]
    for x in fait:
      if id_spots== x:
        les.append(y[1])
  user_spot = {'name': user['name'], 'spots_fait': les}
  user = {'name': user['name'], 'id_spot': fait}

  return redirect('show')

@app.post('/nouveau_spot')
def nouveau_spot():
  spot_name = request.form.get('spot_name', default='*', type=str)
  location = request.form.get('location', default='*', type=str)
  denivele = request.form.get('denivele', default='*', type=str)
  debit = request.form.get('debit', default='*', type=str)


  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  req = "insert into spots( spot_name, location, denivele, debit) values ( ?, ?, ?, ?)"
  cur.execute(req, (spot_name, location, denivele, debit))
  conn.commit()
  conn.close()

  return redirect('ajout')

@app.post('/remove')
def remove():
  global user, user_spot

  spots = []

  rem_spot = request.form["rem_spot"]
  print("supp ", rem_spot)

  conn = sqlite3.connect('app/static/data/database.db')
  cur = conn.cursor()
  cur.execute("DELETE FROM spots WHERE id=?",(rem_spot))
  conn.commit()
  

  id_utilisateur = cur.execute("SELECT id FROM utilisateur").fetchone()
  conn.commit()
  print("id  ", id_utilisateur)
  for i in id_utilisateur:
    spots_utilisateur = cur.execute("SELECT spots_id FROM utilisateur WHERE id=?",(i,)).fetchone()
    if spots_utilisateur == None:
      pass
    else:
      spots_utilisateur_v2 = ""
      print(spots_utilisateur)
      for x in spots_utilisateur:
        print("x ", x)
        if int(rem_spot) > int(x):
          spots_utilisateur_v2 += str(x)
        elif int(rem_spot) < int(x):
          spots_utilisateur_v2 += (str(int(x)-1))
        else:
          pass
    cur.execute("UPDATE utilisateur SET spots_id = ? WHERE id = ?",(spots_utilisateur_v2, str(i)))

  conn.commit() 
  conn.close()

  if user['id_spot'] == None:
    pass
  else:
    for i in user['id_spot']:
      if rem_spot > i:
        spots.append(i)
      elif rem_spot < i:
        spots.append(str(int(i)-1))
      else:
        pass
  
  user['id_spot'] = spots

  return redirect('ajout')
