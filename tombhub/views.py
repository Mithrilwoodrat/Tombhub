# -*- coding: utf-8 -*-
from tombhub import tombhub
from flask import render_template, request, redirect, url_for, jsonify,g
from tombhub import login_manager
from tombhub.models import User
from tombhub.database import db_session
from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@tombhub.before_request
def before_request():
    g.user = current_user

@tombhub.route('/')
def index():
    return render_template("index.html",g=g)

@tombhub.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    print username,passwd
    registered_user = User.query.filter(User.name == username, User.passwd == passwd).first()
    if registered_user is None:
        return jsonify(status="Not Found")#redirect(url_for('login'))
    login_user(registered_user)
    return jsonify(status="login success") #redirect(url_for('index'))


@tombhub.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        passwd = request.form.get('passwd')
        user = User(username, passwd)
        db_session.add(user)
        db_session.commit()
    return render_template('register.html')

@tombhub.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@tombhub.route('/user/<username>')
def user(username):
    return render_template('user.html',username=username)

@tombhub.route('/setting')
@login_required
def setting():
    pass

@tombhub.route('/new_thread', methods=['GET', 'POST'])
@login_required
def new_thread():
    if request.method == 'POST':
        title = request.form.get('title')
        context = request.form.get('editorValue')
        print title,context

    return  render_template('new_thread.html')