import os
import secrets

from PIL import Image
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    pictire_path = os.path.join(current_app.root_path, 'static/images/post_images', picture_fn)
    i = Image.open(form_picture)
    i.save(pictire_path)
    return picture_fn

def delete_picture(old_picture):
    picture_path = os.path.join(current_app.root_path, 'static/images/post_images', old_picture)
    if os.path.exists(picture_path):
        os.remove(picture_path)