import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app
from flask_login import current_user, login_required
from fomo.posts.forms import PostForm
from fomo.models import Post, Venue, Category
from fomo import db
from fomo.posts.utils import save_picture, delete_picture

from fomo.main.forms import testForm

posts = Blueprint('posts', __name__)

@posts.route("/create", methods=['GET','POST'])
@login_required
def create_post():  
    form = PostForm()
    form.venue.choices = [(venue.id, venue.venue_name) for venue in Venue.query.all()]
    form.categories.choices = [(category.id, category.title) for category in Category.query.all()]    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else: 
            picture_file = 'default.jpg'
        
        print(form.start_date.data)
        
        post=Post(title=form.title.data, caption=form.caption.data, start_date=form.start_date.data, 
                end_date=form.end_date.data, author=current_user, image_file=picture_file, venue_id=form.venue.data)

        for category_id in form.categories.data:
            new_category = Category.query.get(category_id) 
            new_category.posts.append(post)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Has Been Created!', 'success') 
        return redirect(url_for('posts.create_post')) 

    return render_template('create_post.html', form=form, title='New Event', legend='New Event')

@posts.route("/event/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', title=post.title, post=post)

@posts.route("/event/change/<int:post_id>")
def update_post_panel(post_id):
    post = Post.query.get_or_404(post_id)   
    return render_template('post.html', title=post.title, post=post)

@posts.route("/event")
@login_required
def view_my_event():
    posts=Post.query.filter_by(user_id=current_user.id).order_by(Post.start_date.desc()).all()
    return render_template('view_my_event.html', posts=posts)

@posts.route("/event/update/<int:post_id>", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) 

    if post.author != current_user:
        abort(403)

    form = PostForm()
    picture_file = post.image_file
    form.venue.choices = [(venue.id, venue.venue_name) for venue in Venue.query.all()]
    form.categories.choices = [(category.id, category.title) for category in Category.query.all()]   

    if form.validate_on_submit():
        if form.picture.data:
            delete_picture(picture_file)
            picture_file = save_picture(form.picture.data)

        db.session.delete(post)

        post=Post(title=form.title.data, caption=form.caption.data, start_date=form.start_date.data, end_date=form.end_date.data,
                  author=current_user, image_file=picture_file, venue_id=form.venue.data)

        for category_id in form.categories.data:
            new_category = Category.query.get(category_id) 
            new_category.posts.append(post)
            
        db.session.add(post)
        db.session.commit()
        flash('Your Post Has Been Updated!', 'success')
        return redirect(url_for('posts.view_my_event', post_id=post_id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.caption.data = post.caption

    return render_template("update_post.html", title='Update Event', form=form, legend='Update Post')

@posts.route("/event/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    delete_picture(post.image_file)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted', 'success')
    return redirect(url_for('posts.view_my_event'))