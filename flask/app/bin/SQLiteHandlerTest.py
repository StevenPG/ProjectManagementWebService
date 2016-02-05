from SQLiteHandler import SQLiteHandler

def main():
    test = SQLiteHandler("test-db")
    print(test.checkTableExists('Cars'))
    print(test.createTable("Students", '(id text, age real)'))
    print(test.getTables())
    print(test.getRowsFromTable('Cars'))
    
if __name__ == '__main__':
    main()
