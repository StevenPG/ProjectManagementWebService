'''
@author: Steven Gantz
@date: 2/4/2016
@file: This file is the main handler for the front facing
 web service. All communication will be done through this
 module and other submodules.
'''

# Web service imports
from flask import Flask
from flask import request

# Database module imports
import sqlite3
from SQLiteHandler import SQLiteHandler

''' Name the application module '''
app = Flask(__name__)
app.config['DEBUG'] = True

# Route past IP address
@app.route('/')
def main():
    return 'Hello, World!'

@app.route('/createaccount')
def createaccount():
    #Retrieve parameters
    user = request.args.get('user')
    passwd = request.args.get('passwd')
    if(user == None):
        user = 'empty'
    if(passwd == None):
        passwd = 'empty'

    handler = SQLiteHandler('PM-Web.db')
    handler.insertIntoTable('User', 'email, password', '"test1", "test2"')
        
    return str(user + passwd)
    
#Implement autorunner when run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0')
