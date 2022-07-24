from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, jsonify, abort
from shop.inventory.models import Products
from flask_login import current_user, login_required
from shop.inventory.forms import ProductsForm, SearchProductForm, ProductTypeChoices, AddProductTypeForm, UnitChoices, \
    AddUnitForm, ProductUpdateForm
from shop import db
from shop.inventory.utils import save_picture
import os

inventory = Blueprint('inventory', __name__)


@inventory.route('/inventory_page')
@login_required
def inventory_page():
    if current_user.account_type != 'admin':
        abort(403)
    return render_template('inventory.html')


@inventory.route('/products', methods=['POST', 'GET'])
@login_required
def products():
    # Check if the user is Admin
    if current_user.account_type != 'admin':
        abort(403)

    form_product_type_choices = [(None, 'Select product type')]
    search = None
    page = request.args.get('page', 1, type=int)
    products = Products.query.filter_by(
        user=current_user).paginate(page=page, per_page=5)
    form = SearchProductForm()
    product_update_form = ProductUpdateForm()
    product_type_choices = ProductTypeChoices.query.filter_by(
        user=current_user)
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

        if search and form.p_type.data:
            try:
                int_search = int(search)
                int_search = '%{0}%'.format(int_search)
                products = Products.query.filter(Products.user == current_user, Products.p_type == form.p_type.data,
                                                 Products.product_id.ilike(int_search)).paginate(page=page, per_page=5)
            except:
                str_search = '%{0}%'.format(search)
                products = Products.query.filter(Products.user == current_user, Products.p_type == form.p_type.data,
                                                 Products.name.ilike(str_search)).paginate(page=page, per_page=5)
            form.search.data = search
        # filter by only search
        elif search and not form.p_type.data:
            try:
                int_search = int(search)
                int_search = '%{0}%'.format(int_search)
                products = Products.query.filter(Products.user == current_user,
                                                 Products.product_id.ilike(int_search)).paginate(page=page, per_page=5)
            except:
                str_search = '%{0}%'.format(search)
                products = Products.query.filter(Products.user == current_user,
                                                 Products.name.ilike(str_search)).paginate(page=page, per_page=5)
            form.search.data = search
        elif not search and form.p_type.data:
            try:
                products = Products.query.filter(Products.user == current_user,
                                                 Products.p_type == form.p_type.data).paginate(page=page, per_page=5)
            except:
                products = Products.query.filter(Products.user == current_user,
                                                 Products.p_type == form.p_type.data).paginate(page=page, per_page=5)
            form.search.data = search
        else:
            pass

    form_product_type_choices = []
    form_unit_choices = []
    # product_type_choices = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id)
    product_type_choices = ProductTypeChoices.query.all()
    for product_type_choice in product_type_choices:
        temp = (product_type_choice.choices, product_type_choice.choices)
        form_product_type_choices.append(temp)

    # initiates 'unit' choices from database
    # unit_choices = UnitChoices.query.filter(UnitChoices.user_id == current_user.id)
    unit_choices = UnitChoices.query.filter()
    for unit_choice in unit_choices:
        temp = (unit_choice.choices, unit_choice.choices)
        form_unit_choices.append(temp)
    product_update_form.unit.choices = form_unit_choices
    product_update_form.p_type.choices = form_product_type_choices
    return render_template('products.html', products=products, form=form, search=search, product_update_form=product_update_form)


@inventory.route('/products/add_products', methods=['GET', 'POST'])
@login_required
def add_products():
    if current_user.account_type != 'admin':
        abort(403)
    # choices for product type and unit
    form_product_type_choices = []
    form_unit_choices = []

    form = ProductsForm()  # Product Form
    p_type_form = AddProductTypeForm()  # Product Type Form
    unitForm = AddUnitForm()  # Unit Form

    # get last product To guess what the next product ID would be
    last_product = Products.query.order_by(
        Products.user_id == current_user.id, Products.product_id.desc()).first()

    # initiates 'product type' choices from database
    # product_type_choices = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id)
    product_type_choices = ProductTypeChoices.query.all()
    for product_type_choice in product_type_choices:
        temp = (product_type_choice.choices, product_type_choice.choices)
        form_product_type_choices.append(temp)

    # initiates 'unit' choices from database
    # unit_choices = UnitChoices.query.filter(UnitChoices.user_id == current_user.id)
    unit_choices = UnitChoices.query.all()
    for unit_choice in unit_choices:
        temp = (unit_choice.choices, unit_choice.choices)
        form_unit_choices.append(temp)
    form.unit.choices = form_unit_choices
    form.p_type.choices = form_product_type_choices

    # if ProductForm is submitted and passes validation
    if form.submit.data and form.validate_on_submit():
        # if form.image.data is None:  # check file choose or not
        #     flash('Please select product image.', 'danger')
        #     return redirect(url_for('inventory.add_products'))
        image_file = 'favicon.ico'
        if form.image.data != None:
            image_file = save_picture(form.image.data)

        # if the chosen product type not existed in the database?
        prod_type = ProductTypeChoices.query.filter_by(
            choices=form.p_type.data)
        if not prod_type:
            flash('Please select a valid product type.', 'danger')
            return redirect(url_for('inventory.add_products'))
        p_type = ProductTypeChoices.query.filter_by(
            choices=form.p_type.data).first()
        product = Products(product_id=form.ID.data, name=form.name.data, image=image_file, p_type=p_type.choices,
                           unit=form.unit.data, price=form.price.data, user=current_user)
        db.session.add(product)
        db.session.commit()
        product = Products.query.filter(Products.product_id == form.ID.data,
                                        Products.user_id == current_user.id).first()
        flash(
            f'Product: {product.product_id}, Name: {product.name} added.', 'success')
        return redirect(url_for('inventory.add_products'))

    # if product type form got submitted and validated
    if p_type_form.pt_submit.data and p_type_form.validate_on_submit():
        pt_exist = ProductTypeChoices.query.filter(
            ProductTypeChoices.choices == p_type_form.product_type.data).first()
        if not pt_exist:
            prod_type_to_commit = ProductTypeChoices(
                choices=p_type_form.product_type.data, user=current_user)
            db.session.add(prod_type_to_commit)
            db.session.commit()
            flash(
                f'Added product type: {prod_type_to_commit.choices}', 'success')
        else:
            flash(
                f'Product type: {p_type_form.product_type.data} already exist.', 'info')
        return redirect(url_for('inventory.add_products'))

    # if Unit form got submitted and validated
    if unitForm.unit_submit.data and unitForm.validate_on_submit():
        unit_exist = UnitChoices.query.filter(
            UnitChoices.choices == unitForm.unit.data).first()
        if not unit_exist:
            unit_to_commit = UnitChoices(
                choices=unitForm.unit.data, user=current_user)
            db.session.add(unit_to_commit)
            db.session.commit()
            flash(f'Added unit: {unit_to_commit.choices}', 'success')
        else:
            flash(f'Unit: {unitForm.unit.data} already exist.', 'info')
        return redirect(url_for('inventory.add_products'))

    # guessing next product ID
    if last_product is None:
        form.ID.data = 1001
    else:
        form.ID.data = last_product.product_id + 1

    return render_template('add_products.html', form=form, p_type_form=p_type_form,
                           product_type_choices=product_type_choices, unitForm=unitForm, unit_choices=unit_choices)


@inventory.route('/products/delete/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.account_type != 'admin':
        abort(403)
    product = Products.query.get_or_404(product_id)
    if product and product.user == current_user:
        # # delete product image
        # image_path = os.path.join(
        #     current_app.root_path, f'static/products_images/', product.image)
        # print('HERE: ', image_path)
        # if os.path.exists(image_path):
        #     os.remove(image_path)
        #     db.session.delete(product)
        #     db.session.commit()
        #     result = f'Product Deleted ID: {product.product_id}'
        #     return jsonify({'status': True, 'result': result})
        if product.image == "favicon.ico":
            db.session.delete(product)
            db.session.commit()
            result = f'Product Deleted ID: {product.product_id}'
            return jsonify({'status': True, 'result': result})
        else:
            result = f'Please try again later or Contact admin.'
            return jsonify({'status': False, 'result': result})
    else:
        result = f'There the product does not exist.'
        return jsonify({'status': False, 'result': result})


@inventory.route('/products/delete_product_type/', methods=['GET', 'POST'])
@login_required
def delete_ptype():
    if current_user.account_type != 'admin':
        abort(403)
    response = {}
    response_list = []
    if request.method == 'POST':
        datas = request.json

        for i, data in enumerate(datas):
            product_type_choice = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id,
                                                                  ProductTypeChoices.id == data['id']).first()
            products = Products.query.filter(Products.p_type == product_type_choice.choices,
                                             Products.user_id == current_user.id).first()

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
@login_required
def edit_products():
    if current_user.account_type != 'admin':
        abort(403)
    if request.method == 'POST':
        try:
            choice_id = request.form['id']
            choice_data = request.form['value']

            print("Product Choice ID: ", choice_id)
            print("Product Choice: ", choice_data)

            if choice_data == "":
                return "The input can't be empty."
            pt_choice = ProductTypeChoices.query.get_or_404(
                choice_id)  # using id
            pt_choice_data = ProductTypeChoices.query.filter(ProductTypeChoices.choices == choice_data,
                                                             ProductTypeChoices.id != choice_id,
                                                             ProductTypeChoices.user_id == current_user.id).first()
            if pt_choice.user_id == current_user:
                return 'You are not authorised for this action.'
            if pt_choice_data:
                return 'Product type already exist.'
            products_ = Products.query.filter_by(
                p_type=pt_choice.choices, user=current_user)
            pt_choice.choices = choice_data
            db.session.commit()

            if products_:
                for pr in products_:
                    pr.p_type = choice_data
                    db.session.commit()
            return 'true'
        except:
            return 'Something went wrong.'


@inventory.route('/products/delete_unit/', methods=['GET', 'POST'])
@login_required
def delete_unit():
    if current_user.account_type != 'admin':
        abort(403)
    response = {}
    response_list = []
    if request.method == 'POST':
        datas = request.json

        for i, data in enumerate(datas):
            unit_choice = UnitChoices.query.filter(UnitChoices.user_id == current_user.id,
                                                   UnitChoices.id == data['id']).first()
            products = Products.query.filter(Products.unit == unit_choice.choices,
                                             Products.user_id == current_user.id).first()

            if unit_choice and products is None:
                db.session.delete(unit_choice)
                response['id'] = data['id']
                response['unit'] = unit_choice.choices
                response['status'] = True
            else:
                response['id'] = data['id']
                response['unit'] = unit_choice.choices
                response['status'] = False
            response_list.append(response)
            response = {}
        db.session.commit()
        return jsonify(response_list)
    else:
        return jsonify(response_list)


@inventory.route('/products/edit_unit', methods=['POST'])
@login_required
def edit_units():
    if current_user.account_type != 'admin':
        abort(403)
    if request.method == 'POST':
        try:
            choice_id = request.form['id']
            choice_data = request.form['value']

            print("Unit Choice ID: ", choice_id)
            print("Unit Choice: ", choice_data)

            if choice_data == "":
                return "The input can't be empty."
            unit_choice = UnitChoices.query.get_or_404(choice_id)  # using id
            unit_choice_data = UnitChoices.query.filter(UnitChoices.choices == choice_data,
                                                        UnitChoices.id != choice_id,
                                                        UnitChoices.user_id == current_user.id).first()
            if unit_choice.user_id == current_user:
                return 'You are not authorised for this action.'
            if unit_choice_data:
                return 'Unit already exist.'
            products_ = Products.query.filter_by(
                unit=unit_choice.choices, user=current_user)
            unit_choice.choices = choice_data
            db.session.commit()

            if products_:
                for pr in products_:
                    pr.unit = choice_data
                    db.session.commit()
            return 'true'
        except:
            return 'Something went wrong.'


@inventory.route('/products/update_product', methods=['POST'])
@login_required
def update_product():
    if current_user.account_type != 'admin':
        abort(403)
    filename = ""
    image_ext = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
    error = []
    file = request.files  # receive file
    data = request.form  # receive the rest data

    name = data['name']
    p_type = data['p_type']
    unit = data['unit']
    price = data['price']
    product_id = data['product_id']

    if name == '' or p_type == '' or unit == '' or price == '':
        error.append("NullError :: The inputs can't be empty.")

    # query product by ID
    product = Products.query.get_or_404(product_id)

    # check error
    # if user has the right to update
    if product.user != current_user:
        error.append(
            "ValidationError :: You don't have the right permission to perform this action.")

    if file['image']:
        image = file['image']
        _, f_ext = os.path.splitext(image.filename)
        print(f_ext)
        if f_ext not in image_ext:
            error.append(
                f'ImageFormatError ::Image format must be in {image_ext}')

    if len(error) == 0:
        if file['image']:
            image = file['image']
            # delete existing product file
            # get old product filename
            path = os.path.join(current_app.root_path,
                                'static/products_images', product.image)
            if os.path.exists(path):
                os.remove(path)
            new_filename = save_picture(image)
            product.image = new_filename
            filename = new_filename

        if data:
            if product.name != name:
                check_product = Products.query.filter(
                    Products.name == name, Products.user_id == current_user.id).first()
                if not check_product:
                    product.name = name
            if product.p_type != p_type:
                product.p_type = p_type
            if product.unit != unit:
                product.unit = unit
            if product.price != price:
                product.price = price
        db.session.commit()
        return jsonify({"result": error, "image_filename": filename})
    else:
        return jsonify({"result": error})
