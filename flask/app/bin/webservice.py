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
import subprocess

''' Name the application module '''
application = Flask(__name__)
application.config['DEBUG'] = True

# Route past IP address
@application.route('/')
def main():
    return 'Hello, World!'

@application.route('/version')
def version():
    return "2.1.1"

@application.route('/genericSelect')
def genericSelect():
    table = request.args.get('table')
    where = request.args.get('where')
    handler = SQLiteHandler('PM-Web.db')
    return str(handler.selectFromTableWhere(table, "*", where))

@application.route('/genericInsert')
def genericInsert():
    table = request.args.get('table')
    where = request.args.get('where')
    columnString = request.args.get('columnString')
    valueString = request.args.get('valueString')

    if(table == None or where == None or columnString == None or valueString == None):
        return "2"
    
    # Add to messaging table
    
    return "0"

@application.route('/accept')
def acceptRequest():
    currentProject = request.args.get('projectid')
    addedUser = request.args.get('addeduser')
    if(currentProject == None or addedUser == None):
        return "2"
    handler = SQLiteHandler('PM-Web.db')
    currentMemberList = handler.selectFromTableWhere(
        "projecttable", "*", "ProjectID=" + str(currentProject))
    memberListasList = list(currentMemberList[0])

    message = ""
    
    # Update the project's memberlist
    initialMemberList = memberListasList[2]
    try:
        if(initialMemberList == ""):
            updateString = 'MemberList="' + \
                           str(addedUser) + '" WHERE ProjectId="' + \
                           str(currentProject) + '"'
            handler.updateRow("ProjectTable", updateString)
        else:
            updateString = 'MemberList="' + \
                           str(initialMemberList) + '--' + \
                           str(addedUser) + '" WHERE ProjectId="' + \
                           str(currentProject) + '"'
            handler.updateRow("ProjectTable", updateString)
    except:
        return "0 - Failed to update project's memberlist" + initialMemberList

    # Update the added user's projectlist
    addedUserProjectList = handler.selectFromTableWhere(
        "usertable", "*", "email=\"" + str(addedUser) + "\"")
    projectListasList = list(addedUserProjectList[0])
    userProjList = projectListasList[6]

    try:
        if(userProjList == ""):
            updateString = 'ProjectList="' + \
                           str(currentProject) + '" WHERE Email="' + \
                           str(addedUser) + '"'
            handler.updateRow("UserTable", updateString)
        else:
            updateString = 'ProjectList="' + \
                           str(userProjList) + '--' + \
                           str(currentProject) + '" WHERE Email="' + \
                           str(addedUser) + '"'
            handler.updateRow("UserTable", updateString)
    except:
        return "0 - Failed to update user's projectlist"

    return "Successfully joined the project!"

@application.route('/removeUser')
def remove():
    currentProject = request.args.get('projectid')
    addedUser = request.args.get('addeduser')
    if(currentProject == None or addedUser == None):
        return "2"
    handler = SQLiteHandler('PM-Web.db')
    currentMemberList = handler.selectFromTableWhere(
        "projecttable", "*", "ProjectID=" + str(currentProject))
    memberListasList = list(currentMemberList[0])
    
    message = ""
    
    # Update the project's memberlist
    initialMemberList = memberListasList[2]

    newMemberList = initialMemberList.replace(addedUser, "")
    
    try:
        updateString = 'MemberList="' + \
                       str(newMemberList) + '" WHERE ProjectId="' + \
                       str(currentProject) + '"'
        handler.updateRow("ProjectTable", updateString)
    except:
        return "0 - Failed to update project's memberlist" + initialMemberList
    
    # Update the added user's projectlist
    addedUserProjectList = handler.selectFromTableWhere(
        "usertable", "*", "email=\"" + str(addedUser) + "\"")
    projectListasList = list(addedUserProjectList[0])
    userProjList = projectListasList[6]

    newProjectList = userProjList.replace(currentProject, "")

    try:
        updateString = 'ProjectList="' + \
                       str(newProjectList) + '" WHERE Email="' + \
                       str(addedUser) + '"'
        handler.updateRow("UserTable", updateString)
    except:
        return "0 - Failed to update user's projectlist"
    
    return "Successfully removed from the project"

@application.route('/getall')
def getall():
    '''
    This route returns a comma seperated list of
    all users in the database.
    '''
    table = request.args.get('table')
    handler = SQLiteHandler('PM-Web.db')
    if(not table == None):
        try:
            users = handler.selectFromTable(table, "*")
        except:
            users = []
    else:
        users = handler.selectFromTable("UserTable", "*")

    return str(users)
    
@application.route('/update')
def update():
    '''
    This route is going to take the get parameters and
    update a specific record inside the database.

    @param table - which table to update the row in
    @param updateString - the entire updatestring to rebuild the row with
    '''
    table = request.args.get('table')
    updateString = request.args.get('updatestring').replace("**", " ")
    if(table == None or updateString == None):
        return "2"
    try:
        handler = SQLiteHandler('PM-Web.db')
        update = handler.updateRow(table, updateString)
    except:
        return "UpdateString: " + updateString
        
    return "1"

@application.route('/select')
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
        return "-1"

    handler = SQLiteHandler('PM-Web.db')
    whereClause = searchRecord + ' = "' + searchString + '"'
    user = handler.selectFromTableWhere(tableString, '*', whereClause)

    #Nothing was found
    if(user == []):
        return "0"
    else:
        return str(user).strip('[(').strip(')]')

@application.route('/insert')
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

    print table, columnString, valueString

    try:
        handler.insertIntoTable(table, columnString, valueString)
    except:
        return "0"

    # Otherwise
    return "1"

@application.route('/createaccount')
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

@application.route('/login')
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
    application.run(host='0.0.0.0')
