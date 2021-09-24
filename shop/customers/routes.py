from flask import Blueprint, render_template
from flask_login import current_user
from flask_login.utils import login_required
from shop.inventory.models import ProductTypeChoices, Products
from flask import request

customer = Blueprint('customer', __name__)

@customer.route('/products/catalog')
@login_required
def catalogue():
    page = request.args.get('page', 1, type=int)
    latest_products = Products.query.order_by(Products.id.desc()).paginate(page=page, per_page=10)
    product_types = ProductTypeChoices.query.all()
    return render_template('catalogue.html', latest_products=latest_products, product_types=product_types)


@customer.route('/products/catalogue/product-types/<string:product_type>')
@login_required
def catalogue_product_types(product_type):
    products = Products.query.filter_by(p_type=product_type)
    return render_template('catalogue_product_types.html', products=products)