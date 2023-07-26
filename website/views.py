
from flask import Flask, Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .model import Store, Customer, Category, Product, Ecom, db
import csv
from datetime import date
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib
matplotlib.use('Agg')
# Agg is matplotlib backend for creating png files


Views = Blueprint("views", __name__)


def Category_warning(id):
    category = Category.query.get(id)
    products = category.catalog
    produce = Product.query.filter(Product.category_Id == id).all()
    m = 0
    for pro in produce:
        if pro.stock > 0:
            m += 1
    n = len(produce) - m
    return n


def create_ordercsv():
    with open(Path('website/static', 'orders.csv'), 'w', newline='') as orders:
        fieldnames = ['customerid', 'product', 'category',
                      'quantity', 'price', 'purchase date', 'manager_id']
        writer = csv.DictWriter(
            orders, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        orders.close()

   # monthly, weekly business data? Product wise......qty sold in a week or month.....gives estimate of demand for the product
    # Category wise
    # What product sold the most? Qty ---bar chart of all products in a category
    # Highest revenue product? Sale price  ---bar chart of all products in a category


def pd_1():
    Orders_csv = pd.read_csv(Path('website/static', 'orders.csv'))
    Orders_ = pd.DataFrame(Orders_csv)
    Orders_['month'] = Orders_['purchase date'].str[5:7]
    Orders_['month'] = Orders_['month'].astype('int32')
    Orders_['quantity'] = Orders_['quantity'].astype('int32')
    Orders_['price'] = pd.to_numeric(Orders_['price'])
    Orders_['sales'] = Orders_['quantity'] * Orders_['price']

    # Best category for sales
    # Highest grossing Category? ---bar chart of all available categories in manager's portfolio
    # if i didnot do index reset then i am getting no way to access sales amt from this groupby object
    ola = Orders_.groupby('category').sum()['sales'].reset_index()
    cat = ola.category.tolist()
    sale = ola.sales.tolist()

    # print(sale)
    # for item in categorie:
    #     list_.append(item)
    plt.bar(cat, sale)
    plt.xticks(cat)
    plt.ylabel("Total Revenue (Rs)")
    plt.xlabel("Category Name")
    plt.savefig('website/static/BestCategory.png')
    plt.clf()


def pd_2():
    Orders_csv = pd.read_csv(Path('website/static', 'orders.csv'))
    Orders_ = pd.DataFrame(Orders_csv)
    Orders_['month'] = Orders_['purchase date'].str[5:7]
    Orders_['month'] = Orders_['month'].astype('int32')
    Orders_['quantity'] = Orders_['quantity'].astype('int32')
    Orders_['price'] = pd.to_numeric(Orders_['price'])
    Orders_['sales'] = Orders_['quantity'] * Orders_['price']

    # Most recurring Customer
    ola2 = Orders_.groupby('customerid').sum()['sales'].reset_index()
    cat2 = ola2.customerid.tolist()
    sale2 = ola2.sales.tolist()

    # print(ola2)
    # for item in categorie:
    #     list_.append(item)
    plt.bar(cat2, sale2)
    plt.xticks(cat2)
    plt.ylabel("Total Purchases (Rs)")
    plt.xlabel("Customer Id")
    plt.savefig('website/static/BestCustomer.png')
    plt.clf()
    # plt.show()


def pd_3(category):
    product_list = []
    sales_list = []
    Orders_csv = pd.read_csv(Path('website/static', 'orders.csv'))
    Orders_ = pd.DataFrame(Orders_csv)
    Orders_['month'] = Orders_['purchase date'].str[5:7]
    Orders_['month'] = Orders_['month'].astype('int32')
    Orders_['quantity'] = Orders_['quantity'].astype('int32')
    Orders_['price'] = pd.to_numeric(Orders_['price'])
    Orders_['product'] = Orders_['product'].astype('str')
    Orders_['category'] = Orders_['category'].astype('str')
    Orders_['sales'] = Orders_['quantity'] * Orders_['price']

    # Most recurring Customer
    ola3 = Orders_.groupby(['category', 'product']).sum()[
        'sales'].reset_index()
    cat3 = ola3.category.tolist()
    cat4 = ola3['product'].tolist()
    sale3 = ola3.sales.tolist()
    for index, categ in enumerate(cat3):
        if categ == category:
            product_list.append(cat4[index])
            sales_list.append(sale3[index])

    print(product_list)
    print(sales_list)

    plt.bar(product_list, sales_list)
    plt.xticks(product_list)
    plt.ylabel("Total Purchases (Rs)")
    plt.xlabel("Product Name")
    plt.savefig('website/static/BestProduct.png')
    plt.clf()
    # plt.show()


# monthly, weekly business data? Product wise......qty sold in a week or month.....gives estimate of demand for the product

# Category wise
# What product sold the most? Qty ---bar chart of all products in a category
# Highest revenue product? Sale price  ---bar chart of all products in a category
# Highest grossing Category? ---bar chart of all available categories in manager's portfolio


# Landing page
@Views.route('/')
def Home():
    return render_template('landing_page.html')


@login_required
@Views.route('/store/cart')
def Cart():
    print(session['carte'])
    products_cart = []
    grand_total = 0
    if 'carte' not in session:
        session['carte'] = []
    if 'cart' in session:

        # mai baap block hai yeh.....issne jaan nikal di...
        for i, item in enumerate(session['cart']):
            product = Product.query.filter(
                Product.product_id == int(item['id'])).first()
            category = Category.query.filter(
                Category.category_Id == product.category_Id).first()
            category_name = category.category_Name
            manager_id = category.managedBy_Id
            quantity = int(item['quantity'])
            total = product.rate * quantity
            grand_total += total

            products_cart.append({'id': int(product.product_id), 'name': product.product_Name,
                                  'price': product.rate, 'quantity': quantity, 'total': total, 'category': category_name, 'manager_id': manager_id})

        # as a oversight currently added item in product cart is removed cuz session mai next item bhi same id ki hai....toh duplicate items ko add krne ke baad directly weed out bhi kr diya
            n = i+1
            if products_cart:
                for ic in session['cart'][n:]:
                    for it in products_cart:
                        if it["id"] == ic["id"]:
                            products_cart.remove(it)

    session['carte'] = products_cart
    if session['role'] == 'Customer':
        customer_id = session['id']
    else:
        return "Not a customer.So,Cannot Add To Cart", 400
    # print(session['carte'])
    return render_template('cart.html', cart=products_cart, grand_total=grand_total, customer_id=customer_id)


@login_required
@Views.route('/store/cart/remove/<int:id1>')
def Remove_FromCart(id1):
    user_id = session['id']
    grand_total = 0
    res = [sub['id'] for sub in session['carte']]
    print(res)
    res_1 = [sub['id'] for sub in session['cart']]
    print(res_1)
    for i in range(len(res_1)):
        if session['cart'][i]['id'] == id1:
            del session['cart'][i]
            session.modified = True
            break
    print(res_1)
    for i in range(len(res)):
        if session['carte'][i]['id'] == id1:
            del session['carte'][i]
            session.modified = True
            break
    print(res)
# yeh remove functionality ko cart page is integrate krna baki hai
    products_cart = session['carte']
    for item in products_cart:
        grand_total += item['total']

    return render_template('cart.html', cart=products_cart, grand_total=grand_total, customer_id=user_id)


@login_required
@Views.route('/store/cart/checkout/<int:id>')
def Checkout(id):
    list = []
    if session['role'] == 'Customer':
        for item in session['carte']:
            # print(item)
            order = Ecom(quantity_inCart=item['quantity'],
                         product_id=item['id'], customer_id=id, manager_id=item['manager_id'], product_name=item['name'], category_name=item['category'], price_perunit=item['price'])

            product = Product.query.filter(
                Product.product_id == item['id']).first()

            new_stock = product.stock - int(item['quantity'])
            if new_stock >= 0:

                list.append(item)
                db.session.add(order)
                product.stock = new_stock
                db.session.commit()
                continue
            else:
                flash(
                    f"Not enough stock present with us at the moment.Please select lesser quantity for the product/--{ product.product_Name }--\into cart to make order successful.", category='error')
                return redirect(url_for('views.Cart'))
        db.session.commit()

    else:
        session.pop("id")
        session.pop("role")
        session.modified = True
        return "Not a Valid Session.Must Login!", 400
    session.pop("carte")
    session.pop("cart")

    session.modified = True
    print(list)
    date_ = date.today()

    # to add rows to existing csv firl use append ir 'a' instead of writing 'w' ....if u open csv with write it will erase previous data and write only rows in this open window
    with open(Path('website/static', 'orders.csv'), 'a', newline='') as orders:
        fieldnames = ['customerid', 'product', 'category',
                      'quantity', 'price', 'purchase date', 'manager_id']
        writer = csv.DictWriter(
            orders, fieldnames=fieldnames, lineterminator='\n')
# dont use' xx'__'xx ' same quotes for lines with nested quotes...use different quote for inside and outside...so as not to confuse interpreter..used same quote '' for values and dict information wasnot read properly
        for item in list:
            writer.writerow({"customerid": id, "product": item['name'], "category": item['category'],
                             "quantity": item['quantity'], "price": item['price'], "purchase date": str(date_), "manager_id": item['manager_id']})
    orders.close()

    flash("Your order is registerd with the store.We will deliver Shortly.Thanks for your purchase!")
    return redirect(url_for('views.Store_front'))


@login_required
@Views.route('/store', methods=["GET", "POST"])
def Store_front():
    user_id = session['id']
    user_role = session['role']

    if 'carte' not in session:
        session['carte'] = []
    if not session['carte']:
        products_cart_1 = []
    if session['carte']:
        products_cart_1 = session['carte']

    manager_1 = False

    if user_role == 'Customer':
        customer = Customer.query.get(user_id)
        categories_1 = Category.query.all()
        list = []
        if request.method == 'POST' and 'search' in request.form:
            search_ = request.form.get("search")
            if search_.isdigit():
                flash("Incorrect Input. Only accept alphabets", category='error')
                return redirect(url_for('views.Store_front'))

            else:
                # like accepts a regular expression  type formatted search string
                search = '%{}%'.format(search_)
                category_name = Category.query.filter(
                    Category.category_Name.like(search))
                for items in category_name:
                    list.append(items)
                print(list)
                return render_template('storefront.html', categories=list, name=customer.username, id=customer.id, cart=products_cart_1)

        return render_template('storefront.html', categories=categories_1, name=customer.username, id=customer.id, cart=products_cart_1)

    elif user_role == 'Manager':
        manager = Store.query.get(user_id)
        categories = Category.query.filter(
            Category.managedBy_Id == user_id).all()
        manager_1 = True
        list = []
        if request.method == 'POST' and 'search' in request.form:
            search_ = request.form.get("search")
            if search_.isdigit():
                flash("Incorrect Input. Only accept alphabets", category='error')
                return redirect(url_for('views.Store_front'))

            else:
                # like accepts a regular expression  type formatted search string
                search = '%{}%'.format(search_)
                category_name = Category.query.filter(
                    Category.category_Name.like(search))
                for items in category_name:
                    list.append(items)
                print(list)
                return render_template('storefront.html', categories=list, name=manager.username, id=manager.id, cart=products_cart_1, manager_1=manager_1)

        return render_template('storefront.html', categories=categories, name=manager.username, id=manager.id, cart=products_cart_1, manager_1=manager_1)
    else:
        return redirect(url_for("views.landing_page.html"))


@login_required
@Views.route('/store/<category>/products', methods=["GET", "POST"])
def Store_product(category):
    category_1 = Category.query.filter(
        Category.category_Name == category).first()
    products = category_1.catalog
    produce = Product.query.filter(
        Product.category_Id == category_1.category_Id).all()
    m = 0
    for pro in produce:
        if pro.stock > 0:
            m += 1
    products_cart = session['carte']

    if request.method == 'POST' and ('search' in request.form or 'search2' in request.form or 'date' in request.form):
        if 'search' in request.form:
            search_ = request.form.get("search")
        print(search_)
        if 'search2' in request.form:
            search_2 = request.form.get("search2")
        print(search_2)
        if 'date' in request.form:
            date = request.form.get("date")
        print(date)
        if search_:
            list = []
            if search_.isdigit():
                flash("Digits not accepted in namespace", category='error')
                return redirect(url_for('views.Category_catalog', id=category.category_Id))
            elif search_:
                # like accepts a regular expression  type formatted search string
                search = '%{}%'.format(search_)
                product_name = Product.query.filter(
                    Product.product_Name.like(search)).all()
                # print(product_name)
                for pro in product_name:
                    if int(pro.category_Id) == category_1.category_Id:
                        list.append(pro)
                print(list)
                return render_template('product_shop.html', name=category, products=list, product_instock=m, cart=products_cart)
        if search_2:
            list = []
            if search_2.isdigit():
                search_1 = int(search_2)
                print(search_1)

                # this is a cool deep reveal about querying not from the table itself but object...proc becomes a list where all such objects satifying condition gets appended
                for pro in products:
                    if pro.rate == search_1:
                        list.append(pro)

            else:
                flash("Price input must be strictly in digits only.",
                      category='error')
                return render_template('product_shop.html', name=category, products=products, product_instock=m, cart=products_cart)
            return render_template('product_shop.html', name=category, products=list, product_instock=m, cart=products_cart)

        if date:
            list = []

            for pro in products:
                if pro.expiredBy == date:
                    list.append(pro)

            return render_template('product_shop.html', name=category, products=list, product_instock=m, cart=products_cart)

        if search_ == "" or search_2 == "" or date == "":
            return redirect(url_for('views.Store_product', category=category_1.category_Name))

    if request.method == 'POST':
        category_3 = Category.query.filter(
            Category.category_Name == category).first()
        products_1 = category_3.catalog
        product_id = request.form.getlist('product_id')
        qty = request.form.getlist('qty')
        print(qty)
        print(product_id)
        if 'cart' not in session:
            session['cart'] = []

        for index, id in enumerate(product_id):
            if qty[index].isdigit():
                quantity = int(qty[index])
                if quantity > 0:
                    # kyunki fixed value hai toh string type mai store hogi issi liye '' but variable is not string toh not ''
                    session['cart'].append(
                        {'id': int(id), 'quantity': quantity})
        # cuz flask cant detect changes to session when u are using mutable object like list
                    session.modified = True

        category_2 = category_3.category_Id
        produce_1 = Product.query.filter(
            Product.category_Id == category_1.category_Id).all()

        n = 0
        for pro in produce_1:
            if pro.stock > 0:
                n += 1
        products_cart = session['carte']
        print(session['cart'])

        flash("Add3d to Cart.Press Cart icon to view Cart.")

        return render_template('product_shop.html', category=category_2, name=category, products=products_1, product_instock=n, cart=products_cart)
    return render_template('product_shop.html', name=category, products=products, product_instock=m, cart=products_cart)


# login and Logout


@login_required
@Views.route('/manager_dash', methods=["GET", "POST"])
def Dash_manager():
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    list = []
    if os.path.isfile('website/static/BestCategory.png'):
        os.remove('website/static/BestCategory.png')
    pd_1()

    if os.path.isfile('website/static/BestCustomer.png'):
        os.remove('website/static/BestCustomer.png')
    pd_2()

    page_1 = request.args.get('page_1', 1, type=int)
    pagination_1 = Category.query.filter(
        Category.managedBy_Id == manager_id).order_by(
        Category.category_Id).paginate(page=page_1, per_page=4)
    for items in pagination_1:
        n = Category_warning(items.category_Id)
        list.append(n)

    # Pagination of results
    page_2 = request.args.get('page_2', 1, type=int)
    pagination_2 = Ecom.query.filter(Ecom.manager_id == manager_id).order_by(
        Ecom.date_added).paginate(page=page_2, per_page=4)
    categorie = []
    ord = Category.query.all()
    for item in ord:
        nom = item.category_Name
        categorie.append(nom)

    # this statement is wrong cuz list will not be paginated...only applied to db.model class and not relationships
    # orders_received = orders_received_1.query.paginate(per_page=5)

    if request.method == 'POST' and 'cname' in request.form:
        c1 = request.form.get("cname")
        c = Category(category_Name=c1, managedBy_Id=manager_id)
        db.session.add(c)
        db.session.commit()
        # categories = Category.query.filter(
        #     Category.managedBy_Id == manager_id).all()
        return render_template('dash_m.html', categories=pagination_1, name=manager.username, id=manager_id, orders=pagination_2)
    if request.method == 'POST' and 'search' in request.form:
        search_ = request.form.get("search")
        if search_.isdigit():
            search_1 = int(search_)
            # print(search_1)
            category_id = Category.query.filter(
                Category.category_Id == search_1).paginate(page=page_1, per_page=4)

            list = []
            for items in category_id:
                print(items)
                n = Category_warning(items.category_Id)
                list.append(n)

            return render_template('dash_m.html', categories=category_id, name=manager.username, id=manager_id, orders=pagination_2, list=list)

        else:
            # like accepts a regular expression  type formatted search string
            search = '%{}%'.format(search_)
            category_name = Category.query.filter(
                Category.category_Name.like(search)).paginate(page=page_1, per_page=4)
            list = []

            for items in category_name:
                n = Category_warning(items.category_Id)
                list.append(n)
            # print(category)
            return render_template('dash_m.html', categories=category_name, name=manager.username, id=manager_id, orders=pagination_2, list=list)
    if request.method == 'POST' and 'date' in request.form:

        date = request.form.get("date")
        if date == "":
            return redirect(url_for('views.Dash_manager'))
        else:
            order_1 = Ecom.query.filter(
                Ecom.date_added == date).paginate(page=page_2, per_page=4)
            return render_template('dash_m.html', categories=pagination_1, name=manager.username, id=manager_id, orders=order_1, list=list, original=pagination_2)
    return render_template('dash_m.html', categories=pagination_1, name=manager.username, id=manager_id, orders=pagination_2, list=list)


# Manager's DashBoard module
@login_required
@Views.route('/manager_dash/category_create', methods=["GET", "POST"])
def Add_category():
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    if request.method == 'POST':
        cat_name = request.form.get("cname1")
        description = request.form.get("c1name1")
        if len(Category.query.filter_by(category_Name=cat_name).all()) > 0:
            flash(
                "Category name already exists.Use different name.", category='error')
            return render_template('category_form.html', name=manager.username)
        else:
            c = Category(category_Name=cat_name,
                         managedBy_Id=manager_id, description=description)
            db.session.add(c)
            db.session.commit()

            flash("New Category added")
            return redirect(url_for('views.Dash_manager'))

    return render_template('category_form.html', name=manager.username)


@login_required
@Views.route('/manager_dash/category_update/<int:id>', methods=["GET", "POST"])
def Update_category(id):
    user_role = session['role']
    manager_id = session['id']
    manager = Store.query.get(manager_id)
    category = Category.query.get(id)

    if request.method == 'POST':
        m = 0
        name = request.form.get('cname1')
        description = request.form.get('c1name1')

        if not name == "":
            category = Category.query.get(id)
            category.category_Name = name
            db.session.commit()

        if not description == "":
            category = Category.query.get(id)
            category.description = description
            db.session.commit()
        return redirect(url_for('views.Dash_manager'))
    return render_template('category_updateform.html', name=manager.username, variable=id)


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
        expiry = request.form.get("dname1")
        p = Product(product_Name=product_name, metric_Unit=metric, rate=rate,
                    rate_perUnit=rate_unit, stock=inventory, category_Id=id, expiredBy=expiry)
        db.session.add(p)
        category.catalog.append(p)
        db.session.commit()
        return redirect(url_for('views.Dash_manager'))

    return render_template('product_add.html', name=category.category_Name, variable=id)


@login_required
@Views.route('/manager_dash/category_catalog/<int:id>', methods=["GET", "POST"])
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
    if os.path.isfile('website/static/BestProduct.png'):
        os.remove('website/static/BestProduct.png')
    pd_3(category.category_Name)

    if request.method == 'POST':
        if 'search' in request.form:
            search_ = request.form.get("search")
        print(search_)
        if 'search2' in request.form:
            search_2 = request.form.get("search2")
        print(search_2)
        if 'date' in request.form:
            date = request.form.get("date")
        print(date)
        if search_:
            list = []
            if search_.isdigit():
                flash("Digits not accepted in namespace", category='error')
                return redirect(url_for('views.Category_catalog', id=category.category_Id))
            elif search_:
                # like accepts a regular expression  type formatted search string
                search = '%{}%'.format(search_)
                product_name = Product.query.filter(
                    Product.product_Name.like(search)).all()
                # print(product_name)
                for pro in product_name:
                    if int(pro.category_Id) == id:
                        list.append(pro)
                print(list)
                return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=list, product_instock=m)
        if search_2:
            list = []
            if search_2.isdigit():
                search_1 = int(search_2)
                print(search_1)

                # this is a cool deep reveal about querying not from the table itself but object...proc becomes a list where all such objects satifying condition gets appended
                for pro in products:
                    if pro.rate == search_1:
                        list.append(pro)

            else:
                flash("Price input must be strictly in digits only.",
                      category='error')
                return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=products, product_instock=m)
            return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=list, product_instock=m)

        if date:
            list = []

            for pro in products:
                if pro.expiredBy == date:
                    list.append(pro)

            return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=list, product_instock=m)

        if search_ == "" or search_2 == "" or date == "":
            return redirect(url_for('views.Category_catalog', id=category.category_Id))

    return render_template('category_catalog.html', name=category.category_Name, category_id=category.category_Id, products=products, product_instock=m)


@login_required
@Views.route('/delete_account/')
def delete_account():
    user_id = session['id']
    user_role = session['role']
    if user_role == 'Manager':
        user = Store.query.get(user_id)
        categories = Category.query.filter_by(managedBy_Id=user_id).all()
        for cat in categories:
            products = Product.query.filter_by(
                category_Id=cat.category_Id).all()
            for pro in products:
                db.session.delete(pro)
                db.session.commit()
            db.session.delete(cat)
            db.session.commit()
        session.pop("cart", None)
        db.session.delete(user)
        db.session.commit()
    if user_role == 'Customer':
        user = Customer.query.get(user_id)
        orders = Ecom.query.filter_by(customer_id=user_id).all()
        for order in orders:
            db.session.delete(order)
            db.session.commit()
        session.pop("cart", None)
        db.session.delete(user)
        db.session.commit()
    flash("Account Deleted.", category='error')
    return redirect(url_for('views.Home'))


@login_required
@Views.route('/manager_dash/delete_category/<int:id>')
def delete_category(id):
    user_role = session['role']
    if user_role == 'Manager':
        category = Category.query.get(id)
        products = Product.query.filter_by(category_Id=id).all()
        orders = Ecom.query.filter_by(
            category_name=category.category_Name).all()
        for order in orders:
            db.session.delete(order)
            db.session.commit()
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
    user_role = session['role']

    if user_role == 'Manager':
        product = Product.query.get(id)
        orders = Ecom.query.filter_by(product_id=id).all()
        for order in orders:
            db.session.delete(order)
            db.session.commit()
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
            expiry = request.form.get('d1name1')

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
            if not expiry == "":
                product = Product.query.get(id)
                product.expiredBy = expiry
                db.session.commit()

            for pro in produce:
                if pro.stock > 0:
                    m += 1
            return render_template('category_catalog.html', name=category.category_Name, category_id=category_id, products=products, product_instock=m)
    return render_template('update_item.html', name=category.category_Name, variable=category_id, product_id=id)
