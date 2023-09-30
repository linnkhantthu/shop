import os
import secrets
from PIL import Image
from flask import url_for, current_app
from io import StringIO
from shop.inventory.models import Products
from flask_login import current_user


def isAdmin():
    if (current_user.account_type == 'admin'):
        return True
    else:
        return False


def save_picture(form_picture):
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


def isInt(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def isProductExist(product_id):
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
