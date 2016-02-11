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
    uniqueId = request.args.get('id')
    if(user == None):
        user = False
    if(passwd == None):
        passwd = False

    handler = SQLiteHandler('PM-Web.db')
    var = ""
    if(user == False and passwd == False):
       #return str(handler.selectFromTable('UserTable', '*'))
        return str("-1")
    try:
        handler.insertIntoTable('UserTable', 'firstname,lastname,email,password,bio,projectlist,picture', 'null,null,"' + user + '","' + passwd + '",null,null,null')
    except:
        return '1 - User already exists in database'
    
    return '0 - User added to database'

@app.route('/login')
def login():
    #Retrieve parameters
    user = request.args.get('user')
    passwd = request.args.get('passwd')
    if(user == None):
        user = False
    if(passwd == None):
        passwd = False

    handler = SQLiteHandler('PM-Web.db')
    var = ""
    if(user == False and passwd == False):
        return str("-1")

    try:
        user = handler.selectFromTableWhere('UserTable', "*",
                                            'email = "' + user + '" AND ' +
                                            'password = "' + passwd + '"')
        if user == []:
            return "0"
        else:
            return "1"
    except:
        return str("-1")
    

#Implement autorunner when run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0')
