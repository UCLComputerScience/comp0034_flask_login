from flask import Flask, render_template


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500


def create_app(config_class=None):
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)

    # Configure app wth the settings from config.py
    app.config.from_object(config_class)

    # Initialize extensions
    from app.models import db
    with app.app_context():
        db.init_app(app)
        db.create_all()
        populate_db(db)

    # Register Blueprints
    from app.main import bp_main
    app.register_blueprint(bp_main)

    # Register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return app
