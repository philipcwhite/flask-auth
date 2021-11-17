import sqlite3, os
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
        self.con = sqlite3.connect('flask.db')
        self.cursor = self.con.cursor()

    def __del__(self):
        self.con.close()
    
    def create_tables(self):
        create_users = 'CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY, user TEXT, password TEXT);'
        create_nodes = 'CREATE TABLE IF NOT EXISTS nodes (ID INTEGER PRIMARY KEY, name TEXT, ip TEXT, os TEXT);'
        self.cursor.execute(create_users)
        self.cursor.execute(create_nodes)
        self.con.commit()

    def load_data(self):
        insert_nodes = "INSERT INTO nodes VALUES (1, 'test01', '10.0.0.1', 'Linux'),(2, 'test02', '10.0.0.2', 'Windows') ON CONFLICT DO NOTHING;"
        insert_user = "INSERT INTO users VALUES (1, 'admin', 'password') ON CONFLICT DO NOTHING;"
        self.cursor.execute(insert_nodes)
        self.cursor.execute(insert_user)
        self.con.commit()

    def get_nodes(self):
        sql = 'SELECT * FROM nodes;'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_user(self, user, password):
        sql = 'SELECT id FROM users WHERE user=? AND password=?'
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
        for i in rows:
            print(i)
        return render_template('index.html', user = user, rows=rows)

with app.app_context():
    D = Data()
    D.create_tables()
    D.load_data()

if __name__ == '__main__': 
    app.run()
