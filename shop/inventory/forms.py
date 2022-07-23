from itertools import product
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import StringField
from wtforms.fields import IntegerField, SelectField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired, ValidationError
from shop.inventory.models import Products, ProductTypeChoices, UnitChoices
from flask_login import current_user
from flask import flash


class ProductsForm(FlaskForm):
    ID = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(
        ['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG'], DataRequired())])
    p_type = SelectField('Select product type', validators=[DataRequired()])
    unit = SelectField('Select unit', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_ID(self, ID):
        product = Products.query.filter(
            Products.product_id == ID.data, Products.user_id == current_user.id).first()

        if product:
            last_product = Products.query.order_by(Products.user_id == current_user.id,
                                                   Products.product_id.desc()).first()
            raise ValidationError(
                f"This ID is already exist. Recommended: {last_product.product_id + 1}")


class SearchProductForm(FlaskForm):
    '''class Meta:
        csrf = False'''
    search = StringField('Search by ID or Name')
    p_type = SelectField('Search by product type')
    submit = SubmitField('Search')


class AddProductTypeForm(FlaskForm):
    product_type = StringField('Product Type', validators=[DataRequired()])
    pt_submit = SubmitField('Add')

    # def validate_product_type(self, product_type):
    #     # pt_exist = ProductTypeChoices.query.filter(ProductTypeChoices.user_id == current_user.id,
    #     #                                            ProductTypeChoices.choices == product_type.data).first()
    #     pt_exist = ProductTypeChoices.query.filter(ProductTypeChoices.choices == product_type.data).first()
    #     if pt_exist:
    #         raise ValidationError("Product type already exist.")


class AddUnitForm(FlaskForm):
    unit = StringField('Unit', validators=[DataRequired()])
    unit_submit = SubmitField('Add')

    # def validate_product_type(self, unit):
    #     # unit_exist = UnitChoices.query.filter(UnitChoices.user_id == current_user.id,
    #     #                                       UnitChoices.choices == unit.data).first()
    #     unit_exist = UnitChoices.query.filter(UnitChoices.choices == unit.data).first()
    #     if unit_exist:
    #         print("EXIST")
    #         raise ValidationError("Unit already exist.")


class ProductUpdateForm(FlaskForm):
    product_id = IntegerField('ID')
    name = StringField('Name')
    image = FileField('Image')
    p_type = SelectField('Select product type')
    unit = SelectField('Select unit')
    price = IntegerField('Price')
    submit_update_form = SubmitField('Update')

    def validate_name(self, name, product_id):
        product = Products.query.filter(
            Products.name == name, Products.user_id == current_user.id, Products.id != product_id).first()
        if product:
            raise ValidationError("Product name already exist.")
