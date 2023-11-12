
from flask import Flask
from flask import render_template, redirect, request, url_for
import flask_login
import pyodbc
import requests
import json
from json import JSONDecoder

##SQL connection 

server = "tcp:s30.winhost.com"
db = "DB_128040_scri0004"
user = "DB_128040_scri0004_user"
password = "Thomas113366806"

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};port=1433;SERVER='+ server + ';DATABASE=' + db +';UID=' + user + ';PWD=' + password + ';encrypt=no')

#PokemonList Class (retrieves all pokemon and lists them in table)
class PokemonList:
     def __init__(self,pokemonList):
          self.pokemonList = pokemonList

class PokemonListEncoder(JSONDecoder):
     def default(self,o):
          return o.__dict__

#Pokemon Class (individual class for each pokemon)
class Pokemon:
     def __init__(self,name,url,height,weight,types):
          self.name = name
          self.url = url
          self.height = height
          self.weight = weight
          self.types = types

class PokemonEncoder(JSONDecoder):
     def default(self,o):
          return o.__dict__

#Sprite class (to store images for each pokemon)
class Sprite:
     def __init__(self,front_default,back_default):
          self.front_default = front_default
          self.back_default = back_default

class SpriteEncoder(JSONDecoder):
     def default(self,o):
          return o.__dict__
     

#initialize flask app
app = Flask(__name__)



#create login manager for Flask
app.secret_key = 'curlyunicorn632'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#retrieving user account data
accounts = {}


#user class inherited from library
class User(flask_login.UserMixin):
    pass

#login manager that loads uers
@login_manager.user_loader
def user_loader(username):
    # if username not in accounts:
    #     return

    user = User()
    user.id = username
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    error = None
    if request.method == 'POST':
        cursor = conn.cursor()
        accounts = cursor.execute('Select * from Users').fetchall()
        for row in accounts:
             print(row[1],row[2])
             if request.form['username'] == row[1]:
                  if request.form['password'] != row[2]:
                       error = 'The username or password is incorrect'
                  else:
                       user = User()
                       user.id = request.form['username']
                       flask_login.login_user(user)
                       return redirect(url_for('home'))
        error = 'The username or password is incorrect'

     #    if request.form['username'] not in accounts[1]:
     #         error = 'The username or password is incorrect or the account does not exist'
     #    else:
             
     #         password = request.form['password']
             
                   
             

     #    if request.form['username'] != 'admin' or request.form['password'] != 'pokeDex':
     #        error = 'The username or password is incorrect'
     #    else:
     #        return redirect(url_for('home'))
    return render_template('login.html', error=error)



#home page, will show the list of pokemon 
@app.route('/')
@app.route('/home')
def home():
     ##testing SQL Connection
     # cursor = conn.cursor()
     # results = cursor.execute('SELECT * FROM Car').fetchall()
     # for row in results:
     #      print(row[1])
     # cursor.close()

     backgroundColors = {}
     backgroundColors["grass"] = "#AFE1AF"
     backgroundColors["poison"] = "#B24BF3"
     backgroundColors["fire"] = "#FF7500"
     backgroundColors["flying"] = "#C5C5C5"
     backgroundColors["dragon"] = "#FFC270"
     backgroundColors["water"] = "#5DD6F4"
     backgroundColors["bug"] = "#50C878"
     backgroundColors["normal"] = "#C5C5C5"
     #backgroundColors["dark"] = "#"
     backgroundColors["electric"] = "#FFD700"
     backgroundColors["psychic"] = "#9370DB"
     backgroundColors["ground"] = "#FF8C00"
     backgroundColors["ice"] = "#7DF9FF"
     backgroundColors["steel"] = "#A9A9A9"
     backgroundColors["fairy"] = "#FF69B4"
     backgroundColors["fighting"] = "#ff8c00"
     backgroundColors["rock"] = "#E89020"
     backgroundColors["ghost"] = "#8A2BE2"

     #get list of pokemon names (limit to 250)
     url = 'https://pokeapi.co/api/v2/pokemon?offset=0&limit=100'
     req = requests.get(url).json()
     
     #for each pokemon name, fetch the info about them 
     pokemonList = []
     index = 1
     for r in req['results']:
          url2 = 'https://pokeapi.co/api/v2/pokemon/' + r['name']
          req2 = requests.get(url2).json()
          pokemonList.append(req2)
     
     #pass pokemon info to view
     context = {
          "pokemonList": pokemonList,
          "index" : index
     }

     #load home with cards for each roster
     return render_template('home.html',**context, bgColors=backgroundColors)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)