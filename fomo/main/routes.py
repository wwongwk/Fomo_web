from flask import Blueprint, request, render_template, url_for,redirect
from fomo.models import Post, Category, User 
from fomo.main.forms import testForm
from flask_wtf import Form
from fomo.main.utils import save_picture
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from fomo import db, bcrypt

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    categories = Category.query.all()
    posts = Post.query.order_by(Post.start_date.desc()).limit(9)

    category_row_one = [ categories[0],categories[1],categories[2],categories[3],categories[4] ]
    category_row_two = [ categories[5],categories[6],categories[7],categories[8],categories[9] ]

    return render_template('home.html', posts = posts, categories=categories, 
    category_row_one = category_row_one, category_row_two = category_row_two)

@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/test", methods=['GET','POST'])
@login_required
def test():
    form = testForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            
        db.session.commit()
        flash('Your account is updated', 'success')
        return redirect(url_for('main.test'))  

    return render_template('test.html', form=form)