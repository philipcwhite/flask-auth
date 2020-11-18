import pymysql, os
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = os.urandom(12)

def authenticate(func):
    def wrapper(*args, **kwargs):
        if session.get('auth') is None:
            return redirect('/login')
        else: return func(*args, **kwargs)     
    wrapper.__name__ = func.__name__     
    return wrapper     

class Data:
    def __init__(self):
        self.con = pymysql.connect(host = 'localhost', user = 'monitoring', password = 'password', db = 'monitoring', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()
         
    def get_nodes(self):
        sql = 'SELECT * FROM nodes;'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_user(self, user, password):
        sql = 'SELECT id FROM users WHERE user=%s AND password=%s'
        self.cursor.execute(sql, (user, password))
        id = self.cursor.fetchone()
        if not id is None: return True

class Web:
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            D = Data()
            auth = D.get_user(user, password)
            if auth == True:
                session['user'] = user
                session['auth'] = True
                return redirect('/')

    @app.route('/logout')
    def logout():
        session['auth'] = None
        return redirect('/login')
        
    @app.route('/')
    @authenticate
    def home():
        user = session.get('user')
        D = Data()
        rows = D.get_nodes()
        return render_template('index.html', user = user, rows=rows)

if __name__ == '__main__': 
    app.run(port=4000)
