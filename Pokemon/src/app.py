
from flask import Flask
from flask import render_template,session
import flask_login
import pyodbc
import requests
import json

app = Flask(__name__)

#create login manager for Flask
app.secret_key = 'curlyunicorn632'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)





#home page, will show the list of pokemon 
@app.route('/')
@app.route('/home')
def home():
     return
          




if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)