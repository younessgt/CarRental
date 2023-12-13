#!/usr/bin/python3
""" Flask Web app """

from models import storage
from models.location import Location
from models.car import Car
from models.user import User
from flask import Flask, render_template, request, flash, url_for, redirect
import uuid
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user, login_required


app = Flask(__name__)
app.secret_key = 'youness'

login_manager = LoginManager()
login_manager.init_app(app)


# User loader callback
@login_manager.user_loader
def load_user(user_id):
    """ callback used to reload the user
    object from the user ID stored in the session """

    return storage.get(User, user_id)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def home():
    """ home page """
    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)
    cars = storage.all(Car).values()
    cars = sorted(cars, key=lambda k: k.name)
    cache_id = str(uuid.uuid4())

    if current_user.is_authenticated:
        return render_template('index.html', locations=locations,
                               cars=cars, cache_id=cache_id,
                               is_authenticated=current_user.is_authenticated,
                               user_id=current_user.id)

    else:

        return render_template('index.html', locations=locations,
                               cars=cars, cache_id=cache_id,
                               is_authenticated=current_user.is_authenticated)


@app.route('/register', methods=['POST'])
def register():
    """ register form """

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    def is_valid_email(email):
        """ check if the email is valid and have @"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    def is_email_exist(email):
        """ check if email already exists in database """
        user = storage.get_by_email(User, email)

        if user and user.email == email:
            return True
        return False

    def username_exists(username):
        all_users = storage.all(User)
        for user in all_users.values():
            if user.username == username:
                return True
        return False

    if not username:
        flash('Username is required.')
        return redirect(url_for('home', form='signup'))

    if not email:
        flash('Email is required.')
        return redirect(url_for('home', form='signup'))

    if not password or not confirm_password:
        flash('Password fields are required.')
        return redirect(url_for('home', form='signup'))

    # check if password exist
    if password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('home', form='signup'))

    # check email format
    if not is_valid_email(email):
        flash('Invalid email format.')
        return redirect(url_for('home', form='signup'))

    if is_valid_email(email):
        if is_email_exist(email):
            flash("Email already exists.")
            return redirect(url_for('home', form='signup'))

    # check if the username already exists
    if username_exists(username):
        flash('Username already taken.')
        return redirect(url_for('home', form='signup'))

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    storage.new(new_user)
    storage.save()

    flash('User registered successfully!')
    return redirect(url_for('home', form='signin'))


@app.route('/login', methods=['POST'])
def login():
    """login form"""

    username = request.form.get('username')
    password = request.form.get('password')

    user = storage.get_by_username(User, username)

    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('dashboard'))

    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('home') + '?form=signin')


@app.route('/dashboard', methods=['GET'])
# @login_required
def dashboard():
    """ dashboard page """
    if current_user.is_authenticated:
        cars_user = current_user.user_cars
        return render_template("dashboard.html", cars=cars_user,
                               user_id=current_user.id)
    else:
        return redirect(url_for('home') + '?form=signin')


@app.route('/logout')
@login_required
def logout():
    """ logout method """

    logout_user()
    return redirect(url_for("home"))


@app.route('/signin')
def signin():
    return redirect(url_for('home') + '?form=signin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
