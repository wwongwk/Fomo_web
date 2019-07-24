from flask import Blueprint, request, render_template, url_for,redirect
from fomo.models import Post, Category


categories = Blueprint('categories', __name__)

@categories.route("/category/<int:category_id>")
def view_cateogry(category_id):
    category=Category.query.get(category_id)
    return render_template('view_category.html', category=category)