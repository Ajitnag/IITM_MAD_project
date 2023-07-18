from flask_restful import reqparse, Resource, abort, Api
from flask import render_template, request, flash, session, url_for, redirect, Blueprint
from flask_login import login_required, current_user
from .model import Store, Customer, Category, Product, Ecom, db
from flask import current_app as app

apis = Blueprint("api", __name__)
api = Api(app)


@login_required
class Api_storeManager(Resource):
    def delete(self, id):
        user_id = session['id']
        user_role = session['role']
        if user_role == 'Manager':
            user = Store.query.get(int(id))
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
        flash("Deleted Record Successfuly.")
        # return render_template('landing_page.html')
        return {"status": "deleted"}, 202


# # this resource Api_storeManager is accessible from server via this endpoint
api.add_resource(Api_storeManager, "/api/delete_admin/<int:id>")
