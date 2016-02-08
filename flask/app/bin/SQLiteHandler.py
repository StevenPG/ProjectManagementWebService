'''
@author: Steven Gantz
@date: 2/4/2016
@file: This file works as an abstraction layer between 
making SQLite calls for the Project Management Web 
Service application. This allows for easy SQLite3 
calls that will hide away error checking and 
some light database manipulation.
'''

#Import required sqlite3 library for usage
import sqlite3

class SQLiteHandler(object):
    """
    This class allows for easy SQLite3
    calls that will hide away error checking and
    some light database manipulation.
    """

    """ dbName - Name of the database for internal use """

    """ conn - An open handle to the database """
    
    def __init__(self, dbName):
        """ Standard constructor that saves the db name  """
        self.dbName = dbName

    def __connectDB(self):
        """ Open a connection to the database """
        self.conn = sqlite3.connect(self.dbName)

    def __disconnectDB(self):
        """ Close an open connection to the database """
        self.conn.close()

    def insertIntoTable(self, tableName, columns, values):
        """ Insert data into table """
        self.__connectDB()
        cursor = self.conn.cursor()

        cursor.execute('INSERT INTO ' + tableName + ' (' + columns + ') VALUES (' + values + ')')
        
        self.__disconnectDB()

    def selectFromTable(self, tableName, columnName):
        """ Retrieve an array of all values in a row within in a table """
        self.__connectDB()
        cursor = self.conn.cursor()

        cursor.execute('SELECT ' + columnName + ' FROM ' + tableName)
        for row in cursor:
            print '0' + row[0]
            print '1' + row[1]
            

        return 'test'
        
        self.__disconnectDB()

    def deleteFromTable(self, tableName, whereClause):
        """ Delete a row from the database where the clause fits """
        self.__connectDB()
        cursor = self.conn.cursor()

        cursor.execute('DELETE FROM ' + tableName + ' WHERE [' + whereClause + ']')
        
        self.__disconnectDB()

    def createTable(self, tableName, columns):
        """ 
        Create a new table in the SQLite database if it doesn't exist 
        
        @return - True if table is created,
        @return - False if table already exists.
        """
        self.__connectDB()
        cursor = self.conn.cursor()

        # There is no other possible outcome, so we disconnect inside
        if(self.checkTableExists(tableName)):
            self.__disconnectDB()
            return False
        else:
            cursor.execute(' CREATE TABLE ' + tableName + ' ' + columns)
            self.__disconnectDB()
            return True

    def getTables(self):
        """ return a list of all tables in database """
        self.__connectDB()
        cursor = self.conn.cursor()

        tables = []
        for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            # This is the fetched syntax: (u'tableName',)
            tables.append(row)        
        self.__disconnectDB()
        return tables

    def getRowsFromTable(self, tableName):
        """ Return a list of all rows in an input table """
        self.__connectDB()
        cursor = self.conn.cursor()

        rows = []
        cursor.execute('SELECT * FROM ' + tableName)
        for row in cursor.fetchall():
            rows.append(row)
        self.__disconnectDB()
        return rows

    def checkTableExists(self, tableName):
        """ Check if a table exists and return true or false  """
        self.__connectDB()
        cursor = self.conn.cursor()

        for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            # This is the fetched syntax: (u'tableName',)
            if row == (tableName,):
                return True
        return False
        
        self.__disconnectDB()

    
