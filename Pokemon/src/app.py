
from flask import Flask
from flask import render_template,session
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
     def __init__(self,name,url,height,weight):
          self.name = name
          self.url = url
          self.height = height
          self.weight = weight

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


     #get list of pokemon names (limit to 250)
     url = 'https://pokeapi.co/api/v2/pokemon?offset=0&limit=100'
     req = requests.get(url).json()
     
     pokemonList = []
     index = 1
     for r in req['results']:
          url2 = 'https://pokeapi.co/api/v2/pokemon/' + r['name']
          req2 = requests.get(url2).json()
          pokemonNew = Pokemon(r['name'],req2['sprites']['front_default'],req2['weight'],None)
          pokemonList.append(pokemonNew)
     
     
     context = {
          "pokemonList": pokemonList,
          "index" : index
     }

     
     return render_template('home.html',**context)
     
     
          




if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)