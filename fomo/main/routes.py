import json
from flask import Blueprint, request, render_template, url_for,redirect
from fomo.models import Post, Category, User 
from fomo.main.forms import testForm
from flask_wtf import Form
from fomo.main.utils import convert_events
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from fomo import db, bcrypt

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    categories = Category.query.all()
    posts = Post.query.order_by(Post.start_date.desc()).limit(9)

    raw_events_from_db = Post.query.all()
    events_from_db = convert_events(raw_events_from_db)

    category_row_one = [ categories[0],categories[1],categories[2],categories[3],categories[4] ]
    category_row_two = [ categories[5],categories[6],categories[7],categories[8],categories[9] ]

    return render_template('home.html', posts = posts, categories=categories, 
    category_row_one = category_row_one, category_row_two = category_row_two,
    events_from_db=json.dumps(events_from_db))

@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/calendar", methods=['GET','POST'])
def calendar():
    raw_events_from_db = Post.query.all()
    events_from_db = convert_events(raw_events_from_db)
    return render_template('calendar.html', events_from_db=json.dumps(events_from_db) )