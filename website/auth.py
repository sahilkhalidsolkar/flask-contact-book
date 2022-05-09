from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exists ,try signing up first', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(email, name, password1, password2)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists ,try logging in', category='error')

        elif len(email) < 4:
            flash('Email should be greater than 3 characters', category='error')
        elif len(name) < 2:
            flash('name should be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')

        elif len(password1) < 7:
            flash('Passwords should be greater than 7 characters', category='error')

        else:
            # add user to database
            new_User = User(email=email, first_name=name,
                            password=generate_password_hash(password1, 'sha256'))
            db.session.add(new_User)
            db.session.commit()
            login_user(new_User, remember=True)

            flash('Account successfully created', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
