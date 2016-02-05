'''
@author: Steven Gantz
@date: 2/4/2016
@file: This file is the main handler for the front facing
 web service. All communication will be done through this
 module and other submodules.
'''

# Web service imports
from flask import Flask

# Database module imports
import sqlite3

''' Name the application module '''
app = Flask(__name__)

# Route past IP address
@app.route('/')
def main():
    return 'Hello, World!'

@app.route('/databasetest')
def dbtest():
    conn = sqlite3.connect('test-db')

    # Create table
    with conn:
        cur = conn.cursor()
        #cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
        cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
        cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
        cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
        cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
        cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
        cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
        cur.execute("INSERT INTO Cars VALUES(8,'Volkswagen',21600)")
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
    return str('test')

#Implement autorunner when run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0')
