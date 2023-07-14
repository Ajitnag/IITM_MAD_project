from website import *
# from website import create_app
# from flask import Flask, render_template, request
#

# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api, Resource, abort

# os and sys module help the developer to get to current directory or some other directory in code

# name = main helps to make sure that we actually ran app.py in this file here and are not importing it from somewhere else
# To run flask webserver
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# also works as store = Flask("store")
# db = SQLAlchemy(app)

# we create two databases to store customers(many to many) and store admin(one to many) differently.....We are going to make two different models
# create a database to the flask app in the current directory
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///storedata.sqlite3"

# # Socket/connector ie intialize our database with the flask application
# db.init_app(app)
# app.app_context().push()
# api.init_app(app)


# making the two modules - model and app as linked via single context...The application should understand that we are working in the same pipeline and not two different files
# An active Flask application context is required to make queries and to access db.engine and db.session. This is because the session is scoped to the context so that it is cleaned up properly after every request or CLI command.


# one2many database for scenario : dB for library then components of lib are categories and books...Multiple books can belong to one category but multiple categories cannot belong to one book...One2Many..Parent-Child relation
