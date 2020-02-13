from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import DevConfig

db = SQLAlchemy()
csrf = CSRFProtect()


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500


def create_app(config_class=DevConfig):
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    csrf.init_app(app)

    from populate_db import populate_db
    from app.models import Teacher, Student, Course, Grade
    with app.app_context():
        db.create_all()
        populate_db()

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    return app
