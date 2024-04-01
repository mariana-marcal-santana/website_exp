from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # for hashing the password
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# defining routes for login, logout and sign up
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # accesses the email from the form
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # gets the first user with the email

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True) # logs in the user
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Email does not exist.", category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first() # gets the first user with the email

        if user:
            flash("Email already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        else:
            # creating a new user and adding it to the database
            new_user = User(email=email, first_name=firstName, last_name=lastName, 
                password=generate_password_hash(password1)) # you can specify a hashing algorithm, i couldn't :)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)