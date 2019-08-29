from flask import render_template, url_for, redirect, flash

from app.main import bp_main
from app.main.forms import SignupForm


@bp_main.route('/')
def index():
    """Renders the homepage as HTML, doesn't use of Jinja2"""
    return render_template('index.html')


@bp_main.route('/hello/')
@bp_main.route('/hello/<name>/')
def hello(name=None):
    """Renders the hello page, uses Jinja2 but doesn't inherit from base template"""
    return render_template('hello.html', name=name)


@bp_main.route('/hello_child/<name>/')
def hello_child(name=None):
    """Renders the hello page with template inheritance which enables message flashing. Used in the signup example"""
    return render_template('hello_child.html', name=name)


@bp_main.route('/signup/', methods=['POST', 'GET'])
def signup():
    """Sign up form, no database interaction"""
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup requested for {}'.format(form.name.data))
        return redirect(url_for('main.hello_child', name=form.name.data))
    return render_template('signup.html', form=form)
