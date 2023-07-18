
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .model import Store, Customer, Category, Product, Ecom, db


Views = Blueprint("views", __name__)

# Landing page


@Views.route('/')
def Home():
    return render_template('landing_page.html')


# login and Logout
@login_required
@Views.route('/manager_dash', methods=["GET", "POST"])
def Dash_manager():
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    categories = Category.query.all()
    if request.method == 'POST':
        c1 = request.form.get("cname")
        c = Category(category_Name=c1, managedBy_Id=manager_id)
        db.session.add(c)
        db.session.commit()
        categories = Category.query.all()
        return render_template('dash_m.html', categories=categories, name=manager.username, id=manager_id)
    return render_template('dash_m.html', categories=categories, name=manager.username, id=manager_id)


@login_required
@Views.route('/customer_dash')
def Dash_customer():
    customer_id = session['id']
    customer = Customer.query.get(customer_id)
    return render_template('dash_c.html', name=customer.username)


# Manager's DashBoard module
@login_required
@Views.route('/manager_dash/category_create', methods=["GET", "POST"])
def Add_category():
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    if request.method == 'POST':
        cat_name = request.form.get("cname1")
        if len(Category.query.filter_by(category_Name=cat_name).all()) > 0:
            flash(
                "Category name already exists.Use different name.", category='error')
            return render_template('category_form.html', name=manager.username)
        else:
            c = Category(category_Name=cat_name, managedBy_Id=manager_id)
            db.session.add(c)
            db.session.commit()
            categories = Category.query.all()
            flash("New Category added")
            return render_template('dash_m.html',  categories=categories, name=manager.username)
    return render_template('category_form.html', name=manager.username)


@login_required
@Views.route('/manager_dash/category_create/<int:id>', methods=["GET", "POST"])
def Add_product(id):
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    category = Category.query.get(id)
    categories = Category.query.all()

    if request.method == 'POST':
        product_name = request.form.get("pname1")
        metric = request.form.get("mname1")
        rate = request.form.get("rname1")
        rate_unit = request.form.get("prname1")
        inventory = request.form.get("sname1")
        p = Product(product_Name=product_name, metric_Unit=metric, rate=rate,
                    rate_perUnit=rate_unit, stock=inventory, category_Id=id)
        db.session.add(p)
        category.catalog.append(p)
        db.session.commit()
        return render_template('dash_m.html',  categories=categories, name=manager.username)
    return render_template('product_add.html', name=category.category_Name, variable=id)


@login_required
@Views.route('/manager_dash/category_catalog/<int:id>')
def Category_catalog(id):
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    category = Category.query.get(id)
    products = category.catalog
    return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=products)


# @login_required
# @Views.route('/manager_dash/update_itemvariables/<int:id>', methods=["GET", "POST"])
# # def Product_item_variables():
# #     manager_id = session['id']
# #     manager = Store.query.get(manager_id)
# #     product = Product.query.get(id)
# #     if request.method == 'POST':
# #         rate = request.form.get("r1name1")
# #         rate_unit = request.form.get("pr1name1")
# #         inventory = request.form.get("s1name1")
# #         if rate:

# #         if rate_unit:
# #         if inventory:
# @login_required
# @Views.route('/delete/<int:id>', methods=['DELETE'])
# def delete_account(id):
#     if request.method == "DELETE":
#         user_id = session['id']
#         user_role = session['role']
#         if user_role == 'Manager':
#             user = Store.query.get(id)
#             categories = Category.query.filter_by(managedBy_Id=id).all()
#             for cat in categories:
#                 products = Product.query.filter_by(
#                     category_Id=cat.category_Id).all()
#                 for pro in products:
#                     db.session.delete(pro)
#                     db.session.commit()
#                 db.session.delete(cat)
#                 db.session.commit()
#             db.session.delete(user)
#             db.session.commit()
#         if user_role == 'Customer':
#             user = Customer.query.get(user_id)
#             db.session.delete(user)
#             db.session.commit()
#         return render_template('landing_page.html')
