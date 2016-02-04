from flask import Flask

'''
@author: Steven Gantz
@date: 2/4/2016
@file: This file is the main handler for the front facing
 web service. All communication will be done through this
 module and other submodules.
'''

''' Name the application module '''
app = Flask(__name__)

# Route past IP address
@app.route('/')
def main():
    return 'Hello, World!'

@app.route('/johncena')
def test():
    return "John Cena"

#Implement autorunner when run locally
if __name__ == '__main__':
    app.run(host='0.0.0.0')
