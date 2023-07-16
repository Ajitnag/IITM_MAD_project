# from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from datetime import datetime
from website import db

# db = SQLAlchemy()
# from sql_alchemy.sql import func
# . stands for current package that we are in ie from __init__.py file import db variable

# db = SQLAlchemy()       #this is a class object


# query.get() method is defined when i knw the primary key like
# Difference b/w invoking method and get value of attrib
# find() is a fn and invoked on object as object.find()
# suppose object has inherent attribute like color...so we can get value of this attribute of object by object.color
# variable = class.query.filter_by(col value).all()
# for items in variable
# it is table name and not class name
# so not use capital letter but small letter
# db.model is a base class used for creating data model ie table
# a table has rows and cols....each row will be a new user/record
# usermixin helps to use flask_login plug and helps to log in / out users easily


# UserMixin is a helper provided by the Flask-Login library to provide boilerplate methods necessary for managing users. Models which inherit UserMixin immediately gain access to 4 useful methods:
# has an is_authenticated() method that returns True if the user has provided valid credentials
# has an is_active() method that returns True if the user’s account is active
# has an is_anonymous() method that returns True if the current user is an anonymous user
# has a get_id() method which, given a User instance, returns the unique ID for that object

# --------------Data Model------------------


class Store(db.Model, UserMixin):
    # manager_Firstname = db.Column(db.String(), nullable=False)
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), nullable=False)
    # manager_Lastname = db.Column(db.String())
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    creates = db.relationship('Category', backref='managedBy')
    # one wali side pe relationship wali statement aur many wali side pe foreign key
    # creates = db.relationship('Category', secondary = 'enrollments', backref= 'managed_By')


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), nullable=False)
    # customer_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    buy = db.relationship('Product', backref='buyer', secondary='ecom')


class Category(db.Model):
    category_Name = db.Column(db.String(), nullable=False, unique=True)
    category_Id = db.Column(db.Integer(), primary_key=True)
    managedBy_Id = db.Column(db.Integer(), db.ForeignKey('store.id'))
#  nullable = False)
# managedBy = db.relationship('Store', backref= 'creates')
    catalog = db.relationship('Product', backref='parent')


class Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True)
    product_Name = db.Column(db.String(), nullable=False)
    metric_Unit = db.Column(db.String(), nullable=False)
    rate = db.Column(db.Integer(), nullable=False)
    rate_perUnit = db.Column(db.String(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    category_Id = db.Column(db.String(), db.ForeignKey('category.category_Id'))
    # parent =  db.relationship('Category', backref= 'catalog')

    # in many2many, using secondary..we capture FK in separate table so less lines of code to be written in parent tables
    # customer_Id = db.Column(db.String(), db.ForeignKey('customer.customer_Id'), nullable = False)
    # buyer = db.relationship('Customer', backref= 'catalog')


class Ecom(db.Model):
    # basket_id = db.Column(db.Integer(), primary_key = True)
    quantity_inCart = db.Column(db.Integer(), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey(
        'product.product_id'), primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey(
        'customer.id'), primary_key=True)


def get_id(self):
    return self.id
# pass around users information across different views/pages we use sessions..sessions are temporary and stored on web server for quick access of inform by diff pages..session is there when user logs in
#  while user is on ur website .sessions are stored on web server and not on client side
