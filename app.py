from flask import Flask, render_template,redirect, url_for, request
import psycopg2
import os
from datetime import datetime


DATABASE = {
'dbname' : os.getenv('DB_NAME'),
'user' : os.getenv('DB_USER'),
'password' : os.getenv('DB_PASSWORD'),
'host' : 'localhost',  
'port' : '5432'  
}    

USERNAME = 'admin'
PASSWORD = 'admin'

app = Flask(__name__)


def authenticate(f):
    """Decorator to enforce authentication on a route."""
    def wrapper(*args, **kwargs):
        auth = request.authorization
        unauthorized_header = {"WWW-Authenticate": "Basic realm='admin_panel'"}
        if not auth:
            return "Username and password Required", 401, unauthorized_header
        if auth.username != USERNAME or auth.password != PASSWORD:
            return "Invalid Credentials", 403, unauthorized_header
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/')
def index():
    global connect
    connect = psycopg2.connect(**DATABASE)
    global db
    db = connect.cursor()
    return redirect(url_for('home'))

@app.route('/home')
def home():
    db.execute('SELECT id, title, date FROM article;')
    post = [{'id': row[0], 'title': row[1], 'date': row[2]} for row in db.fetchall()]
    return render_template('index.html', posts=post)

@app.route('/article/<int:id>')
def view(id):
    db.execute(f'SELECT title, content, date FROM article WHERE id = {id};')
    post = db.fetchone()
    db.close()
    connect.close()
    return render_template('view.html', title=post[0], content=post[1], date=post[2])

@app.route('/admin')
@authenticate
def admin():
    db.execute('SELECT id, title, date FROM article;')
    post = [{'id': row[0], 'title': row[1]} for row in db.fetchall()]
    return render_template('admin.html',posts=post)

@app.route('/new')
@authenticate
def new():
    date = datetime.now().strftime('%Y-%m-%d')
    return render_template('new.html',date=date)

@app.route('/new',methods=['POST'])
@authenticate
def create():
    db.execute('SELECT MAX(id) FROM article;')
    id = db.fetchone()[0] + 1
    title = request.form['title']
    content = request.form['content']
    date = datetime.now().strftime('%Y-%m-%d')
    db.execute('INSERT INTO article (id, title, date, content) VALUES (%s, %s, %s, %s)', (id, title, date, content))
    connect.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:id>')
@authenticate
def delete(id):
    db.execute(f'DELETE FROM article WHERE id = {id};')
    connect.commit()
    return redirect(url_for('admin'))

@app.route('/edit/<int:id>')
@authenticate
def update(id):
    db.execute(f'SELECT id, title, date, content FROM article WHERE id = {id};')
    temp = db.fetchone()
    post = {'id':temp[0],'title': temp[1], 'date': temp[2], 'content': temp[3]}
    return render_template('edit.html', posts=post)

@app.route('/edit/<int:id>', methods=['POST'])
@authenticate
def save(id):
    title = request.form['title']
    content = request.form['content']
    db.execute('UPDATE article SET title = %s, content = %s  WHERE id = %s', (title, content, id))
    connect.commit()
    return redirect(url_for('admin'))
    
if __name__ == '__main__':
    app.run(debug=True)