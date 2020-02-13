from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_wtf.csrf import CSRFError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import with_polymorphic, session

from app import db
from app.main.forms import SignupForm
from app.models import Course, Student, Teacher, User

bp_main = Blueprint('main', __name__)


@bp_main.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


@bp_main.route('/')
def index(name=""):
    return render_template('index.html', name=name)


@bp_main.route('/signup/', methods=['POST', 'GET'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.role.data == "student":
            user = Student(name=form.name.data, email=form.email.data, student_ref=form.uni_id.data)
        else:
            user = Teacher(name=form.name.data, title=form.title.data, teacher_ref=form.uni_id.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('You are now a registered user!')
            return redirect(url_for('main.index'))
        except IntegrityError:
            db.session.rollback()
            flash('ERROR! Unable to register {}. Please check your details are correct and resubmit'.format(
                form.email.data), 'error')
    return render_template('signup.html', form=form)


@bp_main.route('/courses', methods=['GET'])
def courses():
    courses = Course.query.join(Teacher).with_entities(Course.course_code, Course.name,
                                                       Teacher.name.label('teacher_name')).all()
    return render_template("courses.html", courses=courses)


@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter a name to search for")
            return redirect('/')
        users = with_polymorphic(User, [Student, Teacher])
        results = db.session.query(users).filter(or_(users.Student.name.contains(term), users.Teacher.name.contains(term))).all()
        # results = Student.query.filter(Student.email.contains(term)).all()
        if not results:
            flash("No students found with that name.")
            return redirect('/')
        return render_template('search_results.html', results=results)
    else:
        return redirect(url_for('main.index'))


@bp_main.route('/student/<name>')
def show_student(name):
    user = Student.query.filter_by(name=name).first_or_404(description='There is no user {}'.format(name))
    return render_template('show_student.html', user=user)
