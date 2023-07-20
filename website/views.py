
from flask import Flask, Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .model import Store, Customer, Category, Product, Ecom, db


Views = Blueprint("views", __name__)

# Landing page


@Views.route('/')
def Home():
    return render_template('landing_page.html')


@login_required
@Views.route('/customer_dash')
@Views.route('/store')
def Store_front():
    user_id = session['id']
    user_role = session['role']
    if user_role == 'Customer':
        customer = Customer.query.get(user_id)
        categories = Category.query.all()
        return render_template('storefront.html', categories=categories, name=customer.username, id=customer.id)

    # return render_template('storefront.html')


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
    return render_template('storefront.html', name=customer.username)


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
    produce = Product.query.filter(Product.category_Id == id).all()
    m = 0
    for pro in produce:
        if pro.stock > 0:
            m += 1
    return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=products, product_instock=m)


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

@login_required
@Views.route('/delete_account/<int:id>')
def delete_account(id):
    user_id = session['id']
    user_role = session['role']
    if user_role == 'Manager':
        user = Store.query.get(id)
        categories = Category.query.filter_by(managedBy_Id=id).all()
        for cat in categories:
            products = Product.query.filter_by(
                category_Id=cat.category_Id).all()
            for pro in products:
                db.session.delete(pro)
                db.session.commit()
            db.session.delete(cat)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()
    if user_role == 'Customer':
        user = Customer.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
    flash("Account Deleted.", category='error')
    return redirect(url_for('views.Home'))


@login_required
@Views.route('/manager_dash/delete_category/<int:id>')
def delete_category(id):
    user_id = session['id']
    user_role = session['role']
    if user_role == 'Manager':
        category = Category.query.get(id)
        products = Product.query.filter_by(category_Id=id).all()
        for pro in products:
            db.session.delete(pro)
            db.session.commit()
        db.session.delete(category)
        db.session.commit()
        flash("Category Deleted.")
    return redirect(url_for('views.Dash_manager'))


@login_required
@Views.route('/manager_dash/delete_product/<int:id>')
def delete_product(id):
    user_id = session['id']
    user_role = session['role']

    if user_role == 'Manager':
        product = Product.query.get(id)

        # products = Product.query.filter_by(category_Id=id).all()
        # for pro in products:
        #     db.session.delete(pro)
        #     db.session.commit()
        db.session.delete(product)
        db.session.commit()
        flash("Product Removed.")
    return redirect(url_for('views.Dash_manager'))


@login_required
@Views.route('/manager_dash/update_item/<int:id>', methods=["GET", "POST"])
def update_item(id):
    user_role = session['role']
    product_1 = Product.query.get(id)
    category_id = product_1.category_Id
    category = Category.query.get(category_id)
    products = category.catalog

    if user_role == 'Manager':
        if request.method == 'POST':
            m = 0
            name = request.form.get('p1name1')
            metric = request.form.get('m1name1')
            rate = request.form.get('r1name1')
            rate_unit = request.form.get('pr1name1')
            inventory = request.form.get('s1name1')
            # product_2 = Product.query.get(id)
            # print(product_1)
            produce = Product.query.filter(
                Product.category_Id == category_id).all()

            if not name == "":
                product = Product.query.get(id)
                product.product_Name = name
                db.session.commit()
            if metric:
                product = Product.query.get(id)
                product.metric_Unit = metric
                db.session.commit()
            if rate_unit:
                product = Product.query.get(id)
                product.rate_perUnit = rate_unit
                db.session.commit()
            if not rate == "":
                product = Product.query.get(id)
                product.rate = rate
                db.session.commit()
            if not inventory == "":
                product = Product.query.get(id)
                product.stock = inventory
                db.session.commit()

            for pro in produce:
                if pro.stock > 0:
                    m += 1
            return render_template('category_catalog.html', name=category.category_Name, category_id=category_id, products=products, product_instock=m)
    return render_template('update_item.html', name=category.category_Name, variable=category_id, product_id=id)
    # p = Product(product_Name=name, metric_Unit=metric, rate=rate,
    #             rate_perUnit=rate_unit, stock=inventory, category_Id=category_id)
    # db.session.update(p)
    # db.session.commit()
    # if name is not None:
    #     product = Product.query.get(id)
    #     product.product_Name = name
    #     db.session.commit()
    # if metric is not None:
    #     product = Product.query.get(id)
    #     product.metric_Unit = metric
    #     db.session.commit()
    # if rate_unit is not None:
    #     product = Product.query.get(id)
    #     product.rate_perUnit = rate
    #     db.session.commit()
    # if rate is not None:
    #     product = Product.query.get(id)
    #     product.rate = rate_unit
    #     db.session.commit()
    # if stock is not None:
    #     product = Product.query.get(id)
    #     product.stock = stock
    #     db.session.commit()
