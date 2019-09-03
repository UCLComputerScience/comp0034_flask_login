from datetime import timedelta
from urllib.parse import urlparse, urljoin

from flask import render_template, url_for, redirect, request, flash, abort
from flask_login import login_required, logout_user, login_user, current_user

from app.auth import bp_auth
from app.auth.forms import SignupForm, LoginForm
from app.models import Student, db


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url

    return '/'


@bp_auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # user is an instance of the `Student` class
        user = Student.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=2))
        flash('Logged in successfully. {}'.format(user.name))

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('main.index'))

    return render_template('login.html', form=form)


@bp_auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = Student(name=form.name.data, email=form.email.data)
        # Use set_password to ensure the password is hashed
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


"""
The following version of signup was used to demo the cookie creation

@bp_auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie("username", form.name.data)
        return response
    return render_template('signup.html', form=form)
"""
