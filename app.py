from flask import Flask, redirect, render_template, request, session, url_for
import os
from db import init_db, check_account, add_account

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route('/', methods=['GET'])
def get_index():
    if 'username' not in session:
        return redirect(url_for('get_login'))

    return render_template('index.html', username=session['username'])


@app.route('/register', methods=['GET'])
def get_register():
    if 'username' in session:
        return redirect(url_for('get_index'))

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def post_register():
    if 'username' in session:
        return redirect(url_for('get_index'))

    username = request.form.get('username')
    password = request.form.get('password')
    if add_account(username, password):
        return redirect(url_for('get_login'))
    else:
        return render_template('register_failure.html')


@app.route('/login', methods=['GET'])
def get_login():
    if 'username' in session:
        return redirect(url_for('get_index'))

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    if 'username' in session:
        return redirect(url_for('get_index'))

    username = request.form.get('username')
    password = request.form.get('password')
    if check_account(username, password):
        session['username'] = username
        return redirect(url_for('get_index'))
    else:
        return render_template('login_failure.html')


@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect(url_for('get_login'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=31337)
