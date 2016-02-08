import sqlite3

conn = sqlite3.connect('PM-Web.db')
c = conn.cursor()

tables = []
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    # This is the fetched syntax: (u'tableName',)
    tables.append(row)
    
print tables


