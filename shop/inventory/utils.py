import os
import secrets
from PIL import Image
from flask import url_for, current_app
from io import StringIO


def save_picture(form_picture):
    print(form_picture)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/products_images', picture_fn)
    output_size = (360, 360)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn




