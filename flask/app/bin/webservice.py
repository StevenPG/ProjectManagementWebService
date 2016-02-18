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

@app.route('/version')
def version():
    return "0.1.4"

@app.route('/select')
def select():
    ''' 
    This route is going to search for a record based on
    the parameters given and return the record's entire 
    contents that is stored in the database.

    @param - which record to select from record=
    @param - a search value under seach=
    @param - which table to search
    '''
    searchRecord = request.args.get('record')
    searchString = request.args.get('search')
    tableString = request.args.get('table')
    if(searchString == None or tableString == None or searchRecord == None):
        return "2"

    handler = SQLiteHandler('PM-Web.db')
    whereClause = searchRecord + ' = "' + searchString + '"'
    user = handler.selectFromTableWhere(tableString, '*', whereClause)

    #Nothing was found
    if(user == []):
        return "0"
    else:
        return str(user).strip('[(').strip(')]')

@app.route('/insert')
def insert():
    '''
    This route is going to insert a value into an input table.
    This value will be a row, and syntax must be valid SQL syntax
    for this operation to complete.

    @param SQLString
    @param table
    '''
    valueString = request.args.get('valuestring')
    columnString = request.args.get('columnstring')    
    table = request.args.get('table')

    if( valueString == None or table == None or columnString == None):
        return "2"

    handler = SQLiteHandler('PM-Web.db')
    try:
        handler.insertIntoTable(table, columnString, valueString)
        return "1"
    except:
        return "0 - Value already exists in table"

@app.route('/createaccount')
def createaccount():
    '''
    This method creates an entry in the user table.
    TODO - It should eventually be replaced with a
    a generic insert function
    '''
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
