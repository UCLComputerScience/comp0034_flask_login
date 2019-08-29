from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    grades = db.relationship('Grade', backref=db.backref('students', lazy=True))

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Student {}>'.format(self.name)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    courses = db.relationship('Course', backref='teachers', lazy=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Teacher {}>'.format(self.name)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    grades = db.relationship('Grade', backref=db.backref('courses', lazy=True))

    def __init__(self, id, name, teacher_id):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id

    def __repr__(self):
        return '<Course {}>'.format(self.name)


class Grade(db.Model):
    __tablename__ = 'grades'

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, primary_key=True)
    grade = db.Column(db.Text)

    def __init__(self, student_id, course_id, grade):
        self.student_id = student_id
        self.course_id = course_id
        self.grade = grade

    def __repr__(self):
        return '<Grade {}>'.format(self.grade)
