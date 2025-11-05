from flask import request, Flask
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    return f'Hello, {username}!'

if __name__ == '__main__':
    app.run(debug=True)