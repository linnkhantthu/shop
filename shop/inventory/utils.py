import os
import secrets
from PIL import Image
from flask import url_for, current_app
from io import StringIO
from shop.inventory.models import Products, ProductTypeChoices, UnitChoices
from flask_login import current_user


def isAdmin():
    if (current_user.account_type == 'admin'):
        return True
    else:
        return False


def isInt(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


class InventoryUtility:
    def __init__(self) -> None:
        pass

    def save_picture(self, form_picture):
        print(form_picture)
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(
            current_app.root_path, 'static/products_images', picture_fn)
        output_size = (360, 360)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        return picture_fn

    def isProductExist(self, product_id):
        try:
            product = Products.query.filter(
                Products.user == current_user, Products.product_id == int(product_id)).count()
        except:
            print("error")
            return False
        if (product == 1):
            return True
        else:
            return False

    def getProductTypeChoices(self):
        choices = []
        product_type_choices = ProductTypeChoices.query.filter(
            ProductTypeChoices.user == current_user)
        for product_type_choice in product_type_choices:
            temp = (product_type_choice.choices, product_type_choice.choices)
            choices.append(temp)
        return choices

    def getUnitChoices(self):
        choices = []
        unit_choices = UnitChoices.query.filter(
            UnitChoices.user == current_user)
        for unit_choice in unit_choices:
            temp = (unit_choice.choices, unit_choice.choices)
            choices.append(temp)
        return choices
