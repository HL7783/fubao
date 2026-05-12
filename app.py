from flask import Flask, redirect, render_template, request, session, url_for
import os
from db import init_db, check_account, add_account, get_all_posts, create_post, \
    get_post_by_post_id, update_post, delete_post

app = Flask(__name__)
app.secret_key = os.urandom(32)


@app.route('/', methods=['GET'])
def get_index():
    if 'username' not in session:
        return redirect(url_for('post_login'))

    return render_template('index.html', username=session['username'])



@app.route('/posts', methods=['GET'])
def get_posts():
    if 'username' not in session:
        return redirect(url_for('post_login'))
    
    posts = get_all_posts()
    return render_template('posts.html', posts=posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def a_posts_new():
    if 'username' not in session:
        return redirect(url_for('post_login'))
    
    if request.method =='POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author_id = session['username']
        create_post(title, content, author_id)
        return redirect(url_for('get_posts'))
    
    return render_template('post_new.html')


@app.route('/posts/<post_id>', methods=['GET'])
def get_posts_post_id(post_id):
    if 'username' not in session:
        return redirect(url_for('post_login'))
    
    post = get_post_by_post_id(post_id)
    if post:
        return render_template('posts.html', posts=posts)
    else:
        return redirect(url_for('get_posts'))    
    
@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if 'username' not in session:
        return redirect(url_for('post_login'))
    
    post = get_post_by_post_id(post_id)
    if not post: return redirect(url_for('get_posts'))
    if post[3] != session['username']: return render_template('post_edit_failure.html')

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        update_post(post_id, title, content)
        return redirect(url_for('get_posts_post_id', post_id=post_id))

    return render_template('post_edit.html', posts=posts)

@app.route('/posts/<post_id>/delete', methods=['GET'])
def get_posts_post_id_delete(post_id):
    if 'username' not in session:
        return redirect(url_for('post_login'))

    post = get_post_by_post_id(post_id)
    if not post:
        return redirect(url_for('get_posts'))

    if post[3] != session['username']:
        return render_template('post_delete_failure.html')

    return render_template('post_delete.html', post=post)


@app.route('/posts/<post_id>/delete', methods=['POST'])
def post_posts_post_id_delete(post_id):
    if 'username' not in session:
        return redirect(url_for('post_login'))

    post = get_post_by_post_id(post_id)
    if not post:
        return redirect(url_for('get_posts'))

    if post[3] != session['username']:
        return render_template('post_delete_failure.html')

    delete_post(post_id)
    return redirect(url_for('get_posts'))


@app.route('/register', methods=['POST', 'GET'])
def post_register():
    if 'username' in session:
        return redirect(url_for('get_index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if add_account(username, password):
            return redirect(url_for('post_login'))
        else:
            return render_template('register_failure.html')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def post_login():
    if 'username' in session:
        return redirect(url_for('get_index'))

    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = check_account(username, password)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('get_index'))
        else:
            return render_template('login_failure.html')
    
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    return redirect(url_for('post_login'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=31337)
