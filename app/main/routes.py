import datetime

from flask import render_template, url_for, redirect, make_response, request
from flask_login import current_user

from app.main import bp_main


@bp_main.route('/')
def index(name=None):
    # To read a cookie, access the request object
    if current_user.is_authenticated:
        return render_template('index.html', name=current_user.name)
    if request.cookies.get('username'):
        name = request.cookies.get('username')
    return render_template('index.html', name=name)


@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    # To delete a cookie, set its expiration as a date in the past
    response.set_cookie('username', '', expires=datetime.datetime.now())
    return response


"""
Moved to auth

@bp_main.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        '''To set a cookie, create a response, set the cookie for the response then return the response'''
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie("username", form.name.data)
        return response
    return render_template('signup.html', form=form)
"""
