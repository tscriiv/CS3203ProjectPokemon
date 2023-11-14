
from flask import Flask
from flask import render_template, redirect, request, url_for, jsonify
import flask_login
import psycopg2
import requests
from json import JSONDecoder

from flask_login import login_user, UserMixin, login_required, logout_user, current_user

##POSTGRESSQL connection
# use 'localhost' when running within IDE
# use 'pokemon-db-1' when running within Docker
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'pokeDex_admin'
DB_PASSWORD = ''
DB_NAME = 'poke_dex'

def connect_to_db():
     try:
          connection = psycopg2.connect(
               host=DB_HOST,
               port=DB_PORT,
               user=DB_USER,
               password=DB_PASSWORD,
               database=DB_NAME
          )
          return connection
     except psycopg2.Error as e:
          print("Unable to connect to the database")
          print(e)
          return None

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
login_manager.login_view = 'login'

#retrieving user account data
accounts = {}

#user class inherited from library
class User(UserMixin):
     def __init__(self, user_id, username):
          self.id = user_id
          self.username = username

@login_manager.user_loader
def load_user(user_id):
     # Load a user from the database based on user_id
     connection = connect_to_db()
     if connection is None:
          return None

     try:
          cursor = connection.cursor()
          cursor.execute("SELECT user_id, username FROM users WHERE user_id = %s", (user_id,))
          user_data = cursor.fetchone()

          if user_data:
               return User(user_id=user_data[0], username=user_data[1])

     except psycopg2.Error as e:
          print("Error loading user from the database")
          print(e)
     finally:
          cursor.close()
          connection.close()

     return None

def validate_user_credentials(username, password):
     # Load a user from the database based on user_id
     connection = connect_to_db()
     if connection is None:
          return None

     try:
          cursor = connection.cursor()
          cursor.execute("SELECT user_id, username FROM users WHERE username = %s AND password = %s", (username, password,))
          user_data = cursor.fetchone()

          if user_data:
               return User(user_id=user_data[0], username=user_data[1])

     except psycopg2.Error as e:
          print("Error validating user from the database")
          print(e)
     finally:
          cursor.close()
          connection.close()

     return None

@app.route('/login', methods=['GET', 'POST'])
def login():
     error = None
     if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')

          # Validate credentials (replace with your actual authentication logic)
          user = validate_user_credentials(username, password)
          if user:
               login_user(user)
               return redirect(url_for('home'))
          else:
               error = 'Invalid Credentials. Please try again.'

     return render_template('login.html', error=error)

#home page, will show the list of pokemon 
@app.route('/')
@app.route('/home')
@login_required
def home():

     backgroundColors = {}
     backgroundColors["grass"] = "#AFE1AF"
     backgroundColors["poison"] = "#B24BF3"
     backgroundColors["fire"] = "#FF7500"
     backgroundColors["flying"] = "#C5C5C5"
     backgroundColors["dragon"] = "#FFC270"
     backgroundColors["water"] = "#5DD6F4"
     backgroundColors["bug"] = "#50C878"
     backgroundColors["normal"] = "#C5C5C5"
     backgroundColors["dark"] = "#708090"
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
     
     pokemonList = []
     index = 1
     for r in req['results']:
          url2 = 'https://pokeapi.co/api/v2/pokemon/' + r['name']
          req2 = requests.get(url2).json()
          pokemonList.append(req2)

     #grab roster from db
     rosterList = get_roster_list(current_user.id)
     
     context = {
          "pokemonList": pokemonList,
          "rosterList": rosterList,
          "index" : index
     }
     
     return render_template('home.html',**context, bgColors=backgroundColors)

def get_roster_list(user_id):
     rosterList = []
     # Connect to the PostgreSQL database
     connection = connect_to_db()
     if connection is None:
          return "Error connecting to the database"

     try:
          # Create a cursor to interact with the database
          cursor = connection.cursor()

          cursor.execute("SELECT roster_id, pokemon_url FROM rosters where user_id = %s", (user_id,))

          # Fetch all rows
          rows = cursor.fetchall()
          for r in rows:
               req2 = requests.get(r[1]).json()
               rosterList.append(req2)

          # Close the cursor and connection
          cursor.close()
          connection.close()

     except psycopg2.Error as e:
          print("Error executing SQL query")
          print(e)
          # Close the cursor and connection in case of an error
          cursor.close()
          connection.close()
          return "Error executing SQL query"
     return rosterList

@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(url_for('login'))

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5200, debug=True)