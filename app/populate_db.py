from app.models import Student, Teacher, Course, Grade


def populate_database(db):
    """Populates the simpsons.db database if it is empty

    :return: None
    """

    if not Student.query.first():
        db.session.add_all([Student(id=123, name='Bart', email='bart@fox.com', password='bartman'),
                            Student(id=404, name="Ralph", email="ralph@fox.com", password="catfood"),
                            Student(id=456, name="Milhouse", email="milhouse@fox.com", password="fallout"),
                            Student(id=888, name="Lisa", email="lisa@fox.com", password="vegan")])
    if not Teacher.query.first():
        db.session.add_all([Teacher(id=1234, name="Krabappel"),
                            Teacher(id=5678, name="Hoover"),
                            Teacher(id=9012, name="Stepp")])

    if not Course.query.first():
        db.session.add_all([Course(id=10001, name="Computer Science 142", teacher_id=1234),
                            Course(id=10002, name="Computer Science 143", teacher_id=5678),
                            Course(id=10003, name="Computer Science 190M", teacher_id=9012),
                            Course(id=10004, name="Informatics 100", teacher_id=1234)])

    if not Grade.query.first():
        db.session.add_all([Grade(student_id=123, course_id=10001, grade="B-"),
                            Grade(student_id=123, course_id=10002, grade="C"),
                            Grade(student_id=456, course_id=10001, grade="B+"),
                            Grade(student_id=888, course_id=10002, grade="A+"),
                            Grade(student_id=888, course_id=10003, grade="A+"),
                            Grade(student_id=404, course_id=10004, grade="D+"),
                            Grade(student_id=404, course_id=10002, grade="B"),
                            Grade(student_id=456, course_id=10002, grade="D-")])

    db.session.commit()


