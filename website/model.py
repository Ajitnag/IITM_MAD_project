# from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from datetime import date
from flask_sqlalchemy import SQLAlchemy
# from flask import current_app as app

db = SQLAlchemy()  # this is a class object

# . stands for current package that we are in ie from __init__.py file import db variable


# --------------Data Model------------------


class Store(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.Date, default=date.today())
    creates = db.relationship('Category', backref='managedBy')
    # one wali side pe relationship wali statement aur many wali side pe foreign key
    # creates = db.relationship('Category', secondary = 'enrollments', backref= 'managed_By')


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.Date, default=date.today())
    buy = db.relationship('Product', backref='buyer', secondary='ecom')


class Category(db.Model):
    category_Name = db.Column(db.String(), nullable=False, unique=True)
    category_Id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String())
    managedBy_Id = db.Column(db.Integer(), db.ForeignKey('store.id'))
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
    # buyer = db.relationship('Customer', backref= 'catalog')

    # in many2many, using secondary..we capture FK in separate table so less lines of code to be written in parent tables
    # customer_Id = db.Column(db.String(), db.ForeignKey('customer.customer_Id'), nullable = False)


class Ecom(db.Model):
    # basket_id = db.Column(db.Integer(), primary_key = True)
    quantity_inCart = db.Column(db.Integer(), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey(
        'product.product_id'), primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey(
        'customer.id'), primary_key=True)
    manager_id = db.Column(db.Integer(), nullable=False)
    product_name = db.Column(db.String(), nullable=False)
    date_added = db.Column(db.Date, default=date.today())


# pass around the users information across different views/pages we use sessions..sessions are temporary and created on web server for quick access of logged in user by diff pages


def get_id(self):
    # available method from usermixin class
    return self.id
