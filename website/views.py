# will contain all the routes/views related to application pages like homepage , user profile page etc.
# so we create a Blueprint inside views...Blueprint will store diff views/routes. To connect this blueprint file with the flask application we go to init.py file and make connection there via importing this variable Views
# and register our blueprint here with that flask application
from flask import Blueprint, render_template, request, flash, session, url_for
from flask_login import login_required, current_user


Views = Blueprint("views", __name__)


@Views.route('/')
def Home():
    return render_template('landing_page.html')

# if if didnot import flask_login module here on this page...then it wont work even though i am importing .auth....so to run functions and method on a page it is reqd to import module particualr on that page too.


@login_required
@Views.route('/manager_dash')
def Dash_manager():
    if current_user.is_authenticated():
        user = current_user.username
    return render_template('dash_m.html', name=user)


@login_required
@Views.route('/customer_dash')
def Dash_customer():
    if current_user.is_authenticated():
        user = current_user.username
    return render_template('dash_c.html', name=user)

# ---------------Controller-----------------

# login module
# @app.route('/' , methods = ["GET","POST"])
# will need a serializer or validator that validates the login input is ASCII

# Manager's DashBoard module - Pg 2 after login

# Routes/Views
# @app.route('/store_admin', methods=["GET", "POST"])
# def dash():
#     name = Store.manager_Firstname
#     categories = Category.query.all()
#     if request.method == 'POST':
#         c1 = request.form.get("cname")
#         c = Category(category_Name=c1, managedBy_Id=1)
#         db.session.add(c)
#         db.session.commit()
#         categories = Category.query.all()
#         return render_template('dash_m.html', categories=categories, name=name)
#     return render_template('dash_m.html', categories=categories, name=name)


# @app.route('/category_create')
# def create_category():
#     return render_template('category_form.html')


# def home():
#     # if request.method == "POST":
#     #     role = request.form.get('ID')
#     #     text = request.form.get('id_value')

# @app.route('/manager' , methods = ["GET","POST"])
# def dash():
