import os
import secrets

from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from fomo import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    pictire_path = os.path.join(current_app.root_path, 'static/images/post_images', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pictire_path)
    return picture_fn