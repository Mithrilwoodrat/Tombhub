# -*- coding: utf-8 -*-
from tombhub import tombhub
from flask import render_template, request, redirect, url_for, jsonify,g, Markup, abort
from tombhub import login_manager
from tombhub.models import User, Thread
from tombhub.database import db_session
from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(id):
    return db_session.query(User).get(int(id))

@tombhub.before_request
def before_request():
    g.user = current_user

@tombhub.route('/')
def index():
    threads = db_session.query(Thread).order_by(Thread.created_date.desc()).limit(20).all()
    return render_template("index.html",g=g,threads=threads)

@tombhub.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        registered_user = db_session.query(User).filter(User.name == username, User.passwd == passwd).first()
        if registered_user is None:
            return jsonify(status="FAILED",error="user not found")
        login_user(registered_user)
        return jsonify(status="SUCCESS")
    return render_template('login.html')

@tombhub.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        if db_session.query(User).filter(User.name == username).first():
            return jsonify(status='FAILED',error='user existed')
        else:
            user = User(username, passwd)
            db_session.add(user)
            db_session.commit()
            return  jsonify(status='SUCCESS')
    return render_template('register.html')

@tombhub.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@tombhub.route('/user/<username>')
def user(username):
    user_threads = db_session.query(Thread).order_by(Thread.created_date.desc()).filter(
        Thread.author_name == username).limit(5).all()
    return render_template('user.html', username=username, threads=user_threads)

@tombhub.route('/setting')
@login_required
def setting():
    pass

@tombhub.route('/new_thread', methods=['GET', 'POST'])
@login_required
def new_thread():
    if request.method == 'POST':
        title = request.form.get('title')
        title = Markup(title)
        author = g.user.get_id()
        content = request.form.get('editorValue')
        content = Markup(content)
        if title and content:
            thread = Thread(title, author, content)
            db_session.add(thread)
            db_session.commit()
            return jsonify(status="SUCCESS")
        else:
            return jsonify(status="FAILED")
    return  render_template('new_thread.html')

@tombhub.route('/thread/<id>/')
@tombhub.route('/thread/<id>/<action>')
def thread(id, action=None):
    if not action:
        thread = db_session.query(Thread).filter(Thread.id == id).first()
        if thread:
            return render_template('thread.html',thread=thread)
        else:
            abort(404)
            return redirect('/')
    elif action == "delete":
        thread = db_session.query(Thread).filter(Thread.id == id).first()
        if thread and g.user.get_id() == thread.author_id:
            db_session.query(Thread).filter(Thread.id == id).delete()
            return jsonify(status='SUCCESS')
        else:
            return jsonify(status='FAILED',error='operation illegal')