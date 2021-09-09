from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, jsonify
from werkzeug.wrappers import response
from shop.inventory.models import Products
from flask_login import current_user, login_required
from shop.inventory.forms import ProductsForm, SearchProductForm, ProductTypeChoices, AddProductTypeForm, UnitChoices
from shop import db
from shop.inventory.utils import save_picture
import os

inventory = Blueprint('inventory', __name__)


@inventory.route('/inventory_page')
@login_required
def inventory_page():
    return render_template('inventory.html')


@inventory.route('/products', methods=['POST', 'GET'])
@login_required
def products():
    form_product_type_choices = [(None, 'Select product type')]
    search = None
    page = request.args.get('page', 1, type=int)
    products = Products.query.filter_by(user=current_user).paginate(page=page, per_page=5)
    form = SearchProductForm()
    product_type_choices = ProductTypeChoices.query.filter_by(user=current_user)
    for product_type_choice in product_type_choices:
        temp = (product_type_choice.choices, product_type_choice.choices)
        form_product_type_choices.append(temp)
    form.p_type.choices = form_product_type_choices
    if form.validate_on_submit():
        # filter by both args i.e: search and product type
        search = form.search.data
        if search == '':
            # if user didn't give search args
            search = None
        if form.p_type.data == 'None':
            # if user didn't give product type
            form.p_type.data = None

        if form.search.data and form.p_type.data:
            try:
                int_search = int(search)
                int_search = '%{0}%'.format(int_search)
                products = Products.query.filter(Products.user == current_user, Products.p_type==form.p_type.data,Products.product_id.ilike(int_search)).paginate(page=page, per_page=5)
            except:
                str_search = '%{0}%'.format(search)
                products = Products.query.filter(Products.user == current_user, Products.p_type==form.p_type.data, Products.name.ilike(str_search)).paginate(page=page, per_page=5)
            form.search.data = search
        # filter by only search
        elif form.search.data and not form.p_type.data:
            try:
                int_search = int(search)
                int_search = '%{0}%'.format(int_search)
                products = Products.query.filter(Products.user == current_user, Products.product_id.ilike(int_search)).paginate(page=page, per_page=5)
            except:
                str_search = '%{0}%'.format(search)
                products = Products.query.filter(Products.user == current_user, Products.name.ilike(str_search)).paginate(page=page, per_page=5)
            form.search.data = search
        else:
            try:
                products = Products.query.filter(Products.user == current_user, Products.p_type==form.p_type.data).paginate(page=page, per_page=5)
            except:
                products = Products.query.filter(Products.user == current_user, Products.p_type==form.p_type.data).paginate(page=page, per_page=5)
            form.search.data = search

    return render_template('products.html', products=products, form=form, search=search)


@inventory.route('/products/add_products', methods=['GET', 'POST'])
@login_required
def add_products():
    form_product_type_choices = []
    form_unit_choices = []
    form = ProductsForm()
    p_type_form = AddProductTypeForm()
    last_product = Products.query.order_by(Products.user_id==current_user.id, Products.product_id.desc()).first()
    
    product_type_choices = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id)
    for product_type_choice in product_type_choices:
        temp = (product_type_choice.choices, product_type_choice.choices)
        form_product_type_choices.append(temp)
    
    unit_choices = UnitChoices.query.filter(UnitChoices.user_id == current_user.id)
    for unit_choice in unit_choices:
        temp = (unit_choice.choices, unit_choice.choices)
        form_unit_choices.append(product_type_choice)
    form.unit.choices = form_unit_choices
    form.unit.choices = [('PCS', 'PCS')]
    form.p_type.choices = form_product_type_choices

    if form.submit.data and form.validate_on_submit():
        if form.image.data == None:
            flash('Please select product image.', 'danger')
            return redirect(url_for('inventory.add_products'))
        prod_type = ProductTypeChoices.query.filter_by(choices=form.p_type.data)
        if not prod_type:
            flash('Please select a valid product type.', 'danger')
            return redirect(url_for('inventory.add_products'))
        image_file = save_picture(form.image.data)
        p_type = ProductTypeChoices.query.filter_by(choices=form.p_type.data).first()
        product = Products(product_id=form.ID.data, name=form.name.data, image=image_file, p_type=p_type.choices, unit=form.unit.data, price=form.price.data, user=current_user)
        db.session.add(product)
        db.session.commit()
        product = Products.query.filter(Products.product_id==form.ID.data, Products.user_id==current_user.id).first()
        flash(f'Product: {product.product_id}, Name: {product.name} added.', 'success' )
        return redirect(url_for('inventory.add_products'))

    if p_type_form.pt_submit.data and p_type_form.validate_on_submit():
        '''pt_exist = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id, ProductTypeChoices.choices == p_type_form.product_type.data).first()
        if not pt_exist:'''
        prod_type_to_commit = ProductTypeChoices(choices=p_type_form.product_type.data, user=current_user)
        db.session.add(prod_type_to_commit)
        db.session.commit()
        flash(f'Added product type: {prod_type_to_commit.choices}', 'success')
        '''else:
            flash('Product type already exists.', 'danger')'''
        return redirect(url_for('inventory.add_products'))
    if last_product == None:
        form.ID.data = 1001
    else:
        form.ID.data = last_product.product_id + 1
    return render_template('add_products.html', form=form, p_type_form=p_type_form, product_type_choices=product_type_choices)


@inventory.route('/products/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    if product and product.user == current_user:
        # delete product image
        image_path = os.path.join(current_app.root_path, f'static/products_images/', product.image)
        print('HERE: ', image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
            db.session.delete(product)
            db.session.commit()
            flash(f'Product Deleted ID: {product.product_id}', 'success')
            return redirect(url_for('inventory.products'))
        else:
            flash(f'Please try again later or Contact admin.', 'danger')
            return redirect(url_for('inventory.products'))    
    else:
        flash(f'There the product does not exist.', 'danger')
        return redirect(url_for('inventory.products'))


@inventory.route('/products/delete_product_type/', methods=['GET', 'POST'])
def delete_ptype():
    response = {}
    response_list = []
    if request.method == 'POST':
        datas = request.json
        
        for i, data in enumerate(datas):
            product_type_choice = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id, ProductTypeChoices.id == data['id']).first()
            products = Products.query.filter(Products.p_type == product_type_choice.choices, Products.user_id == current_user.id).first()

            if product_type_choice and products == None:
                db.session.delete(product_type_choice)
                response['id'] = data['id']
                response['product_name'] = product_type_choice.choices
                response['status'] = True
            else:
                response['id'] = data['id']
                response['product_name'] = product_type_choice.choices
                response['status'] = False
            response_list.append(response)
            response = {}
        db.session.commit()
        return jsonify(response_list)
    else:
        return jsonify(response_list)

@inventory.route('/products/edit_product_type', methods=['POST'])
def edit_products():
    if request.method == 'POST':
        try:
            choice_id = request.form['id']
            choice_data = request.form['value']

            print("Product Choice ID: ", choice_id)
            print("Product Choice: ", choice_data)
            

            if choice_data == "":
                return "The input can't be empty."
            pt_choice = ProductTypeChoices.query.get_or_404(choice_id) # using id
            pt_choice_data = ProductTypeChoices.query.filter(ProductTypeChoices.choices == choice_data, ProductTypeChoices.id != choice_id, ProductTypeChoices.user_id == current_user.id).first()
            if pt_choice.user_id == current_user:
                return 'You are not authorised for this action.'
            if pt_choice_data:
                return 'Product type already exist.'
            products_ = Products.query.filter_by(p_type=pt_choice.choices, user=current_user)
            pt_choice.choices = choice_data
            db.session.commit()

            if products_:
                for pr in products_:
                    pr.p_type = choice_data
                    db.session.commit()
            return 'true'
        except:
            return 'Something went wrong.'            
