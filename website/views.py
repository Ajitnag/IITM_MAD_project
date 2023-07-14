# will contain all the routes/views related to application pages like homepage , user profile page etc.
# so we create a Blueprint inside views...Blueprint will store diff views/routes. To connect this blueprint file with the flask application we go to init.py file and make connection there via importing this variable Views
# and register our blueprint here with that flask application
from flask import Blueprint, render_template
from flask_login import login_required, current_user


Views = Blueprint("views", __name__)


@Views.route('/home')
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
