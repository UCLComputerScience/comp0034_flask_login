from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()


class Student(UserMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    grades = db.relationship('Grade', backref=db.backref('students', lazy=True))

    def __repr__(self):
        return '<Student {}>'.format(self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    courses = db.relationship('Course', backref='teachers', lazy=True)

    def __repr__(self):
        return '<Teacher {}>'.format(self.name)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    grades = db.relationship('Grade', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return '<Course {}>'.format(self.name)


class Grade(db.Model):
    __tablename__ = 'grades'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, primary_key=True)
    grade = db.Column(db.Text)

    def __repr__(self):
        return '<Grade {}>'.format(self.grade)
