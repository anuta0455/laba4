from flask import Flask, request, render_template, redirect
from flask import session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(20).hex()

users = {}

# Load users from file
with open('users.txt', 'r') as f:
    for line in f:
        username, password = line.strip().split(':')
        users[username] = password

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged', False):
        return redirect('/home')

    try:
        username = request.form['username']
        password = request.form['password']
    except KeyError:
        return redirect('/')

    if username in users and users[username] == password:
        session['logged'] = True
        session.modified = True
        return redirect('/home')
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/home')
def home():
    if not session.get('logged', False):
        return redirect('/')
    return 'Welcome to the home page!'

# Save users to file
def save_users():
    with open('users.txt', 'w') as f:
        for username, password in users.items():
            f.write(f'{username}:{password}\n')

if __name__ == '__main__':
    app.run(debug=True)
