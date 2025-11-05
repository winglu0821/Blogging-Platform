from flask import Flask, render_template,redirect, url_for
import psycopg2
import os

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
    db.execute('SELECT id, title, date FROM article')
    post = [{'id': row[0], 'title': row[1], 'date': row[2]} for row in db.fetchall()]
    return render_template('index.html', posts=post)

@app.route('/article/<int:id>')
def view(id):
    db.execute(f'SELECT title, content, date FROM article WHERE id = {id}')
    post = db.fetchone()
    db.close()
    connect.close()
    return render_template('view.html', title=post[0], content=post[1], date=post[2])

if __name__ == '__main__':
    app.run(debug=True)

