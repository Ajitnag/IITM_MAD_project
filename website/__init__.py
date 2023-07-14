from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta


# init.py makes website folder a python package this means from anyother file we can simply import website folder and the import will give all of the stuff inside this website folder
db = SQLAlchemy()

# instance_path="/website/instance"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storedata.sqlite3"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# # Socket/connector ie intialize our database with the flask application
    db.init_app(app)
    app.app_context().push()
# will allows us to lg users in/out of website and make sure that everytime they come in they dont have to type in their username and psswd
# and they have acces to certain pages if they are logged in  but they cant access certain pages if they arenot logged in
    login_manager = LoginManager()
# if certain user is not logged in then direct him to auth.login page
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # initialized login_manager for our app so it can find suitable things within the app
    # this is an e.g to show that login_manager allows me to access information abt the user from the database ie currently logged in
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id)
    # id is db.integer() but request method sends id as string so need to convert to integer to send to database for query
    # so the session stores data abt user currently logged in and u can access data like username, psswd etc abt current logged in user via login_manger
    # we know whenver a computer goes to a website it has intialized or started a session with that website...imp inf is stored abt computer in the session file used by website so computer dont need to sign in baar baar..session is temporary storage used for login etc

# import Blueprint stored in variable Views from views file...url_prefix will automatically prefix all of the routes inside blueprint with '/'
# using dot before file names cuz we are doing relative import ie imported file and current file both sit inside website package and for relative reference we put dot in front of file name...Other thing only if u are
# inside python pakage ie where __init__.py then u need to use dot before filename for relative reference among files sitting inside same python package
    from .views import Views
    app.register_blueprint(Views, url_prefix='/')

    from .auth import Auth
    app.register_blueprint(Auth, url_prefix='/')

    from .model import Store, Category, Customer, Product, Ecom
    # imported the tables to make part of the flask application
    create_database(app)

    return app


def create_database(app):
    if not path.exists("instance/storedata.sqlite3"):
        db.create_all()
        print("Database created!!")
