
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta, datetime
from flask_cors import CORS, cross_origin
# from website.api import Api_storeManager
from .model import db


# db = SQLAlchemy()

login_manager = LoginManager()


# instance_path="/website/instance

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = '12345'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stored.sqlite3"

    # Flask's SECRET_KEY variable is a string used to encrypt all of our user's passwords (or other sensitive information)

    # # Socket/connector ie intialize plugins with the flask application
    db.init_app(app)
    # api.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    app.app_context().push()

    with app.app_context():
        # import modules ie parts of application
        from website.views import Views
        from website.auth import Auth
        from website.model import Store, Category, Customer, Product, Ecom
        from .api import apis

        # register blueprints with flask application...  In our app, we don't register routes directly to the Flask app — we've registered them to blueprints instead.
        app.register_blueprint(Views, url_prefix='/')
        app.register_blueprint(Auth, url_prefix='/')
        app.register_blueprint(apis, url_prefix='/api')

        # create_database
        if not path.exists("instance/stored.sqlite3"):
            db.create_all()
            print("Database created!!")

    # api.add_resource(Api_storeManager, "/api/delete_admin/<int:id>")
    return app


# def create_database(app):
#     if not path.exists("/website/instance/stored.sqlite3"):
#         db.create_all()
#         print("Database created!!")
