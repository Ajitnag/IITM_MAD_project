from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import timedelta, datetime


# App Factory
# init.py makes website folder a python package this means from anyother file we can simply import website folder and the import will give all of the stuff inside this website folder
# Good software is organized by separation of concerns. It's easy to think of an application as a single entity, yet reality shows us that well-structured apps are collections of standalone modules, services, or classes.
# We can organize our Flask apps via a built-in concept called Blueprints, which are essentially the Flask equivalent of Python modules. Blueprints are intended to encapsulate feature-sized sections of our application.Blueprints keep related logic and assets grouped and separated from one another, which is essential to designing a maintainable project.
# Flask blueprints enable us to organize our applications by grouping logic into subdirectories.
db = SQLAlchemy()
login_manager = LoginManager()

# instance_path="/website/instance"

# App Factory
# why we using blueprint and package.So why would you want to do this?
# Testing. You can have instances of the application with different settings to test every case.
# Multiple instances. Imagine you want to run different versions of the same application. Of course you could have multiple instances with different configs set up in your webserver, but if you use factories, you can have multiple instances of the same application running in the same application process which can be handy.


def create_app():
    # create flask instance
    app = Flask(__name__)
# Flask's SECRET_KEY variable is a string used to encrypt all of our user's passwords (or other sensitive information)
    app.config['SECRET_KEY'] = '12345'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stored.sqlite3"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# # Socket/connector ie intialize plugins with the flask application
    db.init_app(app)
    app.app_context().push()
    # db.create_all()

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # with App.app_context():
    #     from . import views
    #     db.create_all()

# will allows us to lg users in/out of website and make sure that everytime they come in they dont have to type in their username and psswd
# and they have acces to certain pages if they are logged in  but they cant access certain pages if they arenot logged in

# if certain user is not logged in then direct him to auth.login page

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
    with app.app_context():
        # import modules ie parts of application
        from website.views import Views
        from website.auth import Auth
        from website.model import Store, Category, Customer, Product, Ecom
        if not path.exists("instance/stored.sqlite3"):
            db.create_all()
            print("Database created!!")

        # register blueprints with flask application...  In our app, we don't register routes directly to the Flask app — we've registered them to blueprints instead.
        app.register_blueprint(Views, url_prefix='/')
        app.register_blueprint(Auth, url_prefix='/')

    # from .model import Store, Category, Customer, Product, Ecom
    # # imported the tables to make part of the flask application

    return app


# def create_database(app):
