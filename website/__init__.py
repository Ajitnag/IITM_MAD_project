
from flask import Flask
from os import path
from flask_login import LoginManager


login_manager = LoginManager()
app = Flask(__name__)

# instance_path="/website/instance to store db file in different location


def create_app():

    app.config['SECRET_KEY'] = '12345'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stored.sqlite3"

    # The SECRET_KEY is needed to keep the client-side sessions/cookies secure. Choose that key wisely and as hard to guess and complex as possible.

    # # Socket/connector ie intialize plugins with the flask application
    from .model import db
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    app.app_context().push()

    with app.app_context():
        # import modules from within the package file to be registered in flask app
        from website.views import Views
        from website.auth import Auth

        # register blueprints with flask application...  In our app, we don't register routes directly to the Flask app — we've registered them to blueprints instead.
        app.register_blueprint(Views, url_prefix='/')
        app.register_blueprint(Auth, url_prefix='/')

        # create_database
        if not path.exists("instance/stored.sqlite3"):
            db.create_all()
            print("Database created!!")

    return app
