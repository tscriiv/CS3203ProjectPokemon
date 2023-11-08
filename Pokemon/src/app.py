
from flask import Flask
from flask import render_template,session
import flask_login
import pyodbc
import requests
import json

##SQL connection 

server = "tcp:s30.winhost.com"
db = "DB_128040_scri0004"
user = "DB_128040_scri0004_user"
password = "Thomas113366806"

conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};port=1433;SERVER='+ server + ';DATABASE=' + db +';UID=' + user + ';PWD=' + password + ';encrypt=no')


app = Flask(__name__)

#create login manager for Flask
app.secret_key = 'curlyunicorn632'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)





#home page, will show the list of pokemon 
@app.route('/')
@app.route('/home')
def home():
     ##testing SQL Connection
     cursor = conn.cursor()
     results = cursor.execute('SELECT * FROM Car').fetchall()
     for row in results:
          print(row[1])
     cursor.close()
     return "1"
     
     
          




if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5000, debug=True)