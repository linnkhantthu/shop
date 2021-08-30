from shop.user.forms import LoginForm, RegisterationForm
from flask import Blueprint, render_template, flash, url_for, redirect, abort, session
from flask_login import current_user, login_user, login_required, logout_user
from shop import db, bcrypt
from shop.user.models import User

user = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user.username}', 'info')
        return abort(403)
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)


@user.route("/", methods=['GET', 'POST'])
@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {current_user.username}', 'success')
            return redirect(url_for('main.main_page'))
        else:
            flash('Incorrect username or password, please try again.', 'danger')
            return redirect(url_for('user.login'))
    return render_template('login.html', form=form)

@user.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out.", 'info')
    else:
        flash("You are not logged in.", 'danger')
    return redirect(url_for('user.login'))