# comp0034_flask_login
COMP0034 Code to accompany the lecture covering Flask login, sessions and cookies

### Exercise 1: Cookies
1. Create a cookie in the signup route as soon as a new user has been successfully created. The cookie should use the value of the name field from the form to create a cookie called name. 
After creating the cookie, the user should be directed to the home page.

    To set the cookie you need to: 
    - create a response (in this case the response is to redirect to the URL for the home page)
    - set the cookie for the response, the cookie is called `name` and the value for the name is captured in the form.name field.
    - return the response
   e.g. find the correct location in your signup route and add the following (you will also need to add an import `from flask import make_response` to the imports in `routes.py`
    ```python
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie("name", form.name.data)
    return response
    ```
2. Add a new route to delete the cookie, this is just so that we can see the effect on the index page after the cookie is deleted.
    To delete a cookie, you set its expiration as a date in the past.
    ```python
    @bp_main.route('/delete_cookie')
    def delete_cookie():
        response = make_response(redirect(url_for('main.index')))
        response.set_cookie('name', '', expires=datetime.now())
        return response
    ```
3. To see the value of the cookie, let's modify the `index` page to display a welcome message with the name value if a cookie has been set.
To read a cookie, you need to access the request object.
    ```python
    @bp_main.route('/')
    def index(name=""):
       if 'name' in request.cookies:
           name = request.cookies.get('name')
       return render_template('index.html', name=name)
    ```
4. Signup a new user. You should be directed to the `index` page after a successful signup which should have the content "Welcome <name>".
5. Go to http://127.0.0.1:5000/delete_cookie. You should be directed to the `index` page which should now display "Welcome".

### Exercise 2: Configure the app to support the login manager extension
1. Create a session object and a Login object for the app in `app/__init__.py`
It will look something like this:
    ```python
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    
    db = SQLAlchemy()
    login_manager = LoginManager()
    ```
2. Initialise the plugin in the `create_app()` function in the same way as we did for the database e.g. 
    ```python
   def create_app(config_class=DevConfig):
       app = Flask(__name__)
       app.config.from_object(config_class)
   
       db.init_app(app)
       login_manager.init_app(app)
    ```

### Exercise 3: Create a new auth package for our app
1. Create a new Python package for authentication called `auth` inside the `app` package.
2. Create `app/auth/routes.py` and `app/auth/forms.py` 
3. Define a blueprint for auth in in `app/auth/routes.py` e.g.
    ```python
    from flask import Blueprint
   
    bp_auth = Blueprint('auth', __name__)
    ```
4. In `app/__init__.py` register the auth blueprint e.g.
    ```python
    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    from app.auth.routes import bp_auth
    app.register_blueprint(bp_auth)
    ```
4. Move the existing sign up form from `app/main/forms.py` to `app/auth/forms.py`. To do this, place the cursor on the form class name, right click 
5. Move the existing signup route from `app/main/routes.py` to `app/auth/routes.py`
5. Stop and restart Flask. Check that signup still works.

### Exercise 4: Modify the User class to inherit the Flask-Login UserMixin class
The UserMixin class will provide default implementations for the following methods:
- `is_authenticated` a property that is True if the user has valid credentials or False otherwise
- `is_active` a property that is True if the user's account is active or False otherwise
- `is_anonymous` a property that is False for regular users, and True for a special, anonymous user
- `get_id()` a method that returns a unique identifier for the user as a string (unicode, if using Python 2)

Edit the User class in models.py to inherit UserMixin, you will also need to add the relevant import e.g. 
 ```python
    from flask_login import UserMixin
        
    class User(UserMixin, db.Model):
 ```

### Exercise 5: Create a LoginForm class, login form template and a login route
1. Create a LoginForm class in `app/auth/forms.py` e.g.
    ```
    class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember_me = BooleanField('Keep me logged in')
    ```
2. Create a template for the login form `app/templates/login.html`, e.g.
    ```jinja2
    {% extends 'base.html' %}
    {% from "_formhelpers.html" import render_field %}
    {% block title %}Login{% endblock %}
    {% block content %}
    <form method="post" novalidate>
        {{ form.hidden_tag() }}
        <dl>
            {{ render_field(form.email, class='form-control') }}
            {{ render_field(form.password, class='form-control') }}
            {{ render_field(form.remember_me) }}
            <input type=submit value='Login' class='btn btn-primary'>
        </dl>
    </form>
    {% endblock %}
    ```
3. Add a login route to `app/auth/routes.py` e.g.
