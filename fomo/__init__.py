import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from fomo.config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bcrypt = Bcrypt()
admin = Admin()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    bootstrap = Bootstrap(app)

    from fomo.users.routes import users
    from fomo.posts.routes import posts
    from fomo.main.routes import main
    from fomo.categories.routes import categories

    from fomo.models import User, Post, Category, Venue
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(Venue, db.session))

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(categories)

    return app