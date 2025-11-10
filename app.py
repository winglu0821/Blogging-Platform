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

app = Flask(__name__)

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
def admin():
    db.execute('SELECT id, title, date FROM article;')
    post = [{'id': row[0], 'title': row[1]} for row in db.fetchall()]
    return render_template('admin.html',posts=post)

@app.route('/edit/<int:id>')
def edit(id):
    db.execute(f'SELECT title, date, content FROM article WHE   E id = {id}')
    return render_template('edit.html')

@app.route('/new')
def new():
    date = datetime.now().strftime('%Y-%m-%d')
    return render_template('new.html',date=date)

@app.route('/new',methods=['POST'])
def create():
    db.execute('SELECT MAX(id) FROM article;')
    id = db.fetchone()[0] + 1
    title = request.form['title']
    content = request.form['content']
    date = datetime.now().strftime('%Y-%m-%d')
    db.execute('INSERT INTO article (id, title, date, content) VALUES (%s, %s, %s, %s)', (id, title, date, content))
    connect.commit()
    return redirect(url_for('home'))

@app.route('/admin/delete/<int:id>')
def delete(id):
    db.execute(f'DELETE FROM article WHERE id = {id};')
    connect.commit()
    return redirect(url_for('admin'))

# @app.route('/edit/<int:id>', methods=['POST'])
# def update(id):

if __name__ == '__main__':
    app.run(debug=True)

