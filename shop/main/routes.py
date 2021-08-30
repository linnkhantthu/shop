import os
from flask import Blueprint, render_template, url_for, redirect, flash
from flask.templating import render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/main')
@login_required
def main_page():
    if not current_user.is_authenticated:
        flash("Please login to access this page.", 'danger')
        return redirect(url_for('user.login'))
    return render_template('main_page.html')
