from flask import current_app
from fomo import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#association table for Post and Category
PostCategoryRelationTable = db.Table('PostToCategory',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    extend_existing = True
)

class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #password is hashed
    password = db.Column(db.String(60), nullable=False)

    #one to many relationship, reference post class - the events this user creates
    posts = db.relationship('Post', backref='author', lazy=True)

    #one to many relationship, reference post class - the events this user is following
    followed_posts = db.relationship('Post', backref='follower', lazy=True)

    #reset methods
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)
    #end of reset methods

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}','{self.image_file}')"

class Post(db.Model):
    __table_args__ = {'extend_existing': True}     
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    caption = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    #reference user id attribute
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    
    #many to many association with category 
    category = db.relationship("Category", secondary=PostCategoryRelationTable, back_populates='posts', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}')"

class Category(db.Model):
    __table_args__ = {'extend_existing': True}    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship("Post", secondary=PostCategoryRelationTable, back_populates='category', lazy=True)
    def __repr__(self):
        return f"Category('{self.title}','{self.description}')"

class Venue(db.Model):
    __table_args__ = {'extend_existing': True}  
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content_picture = db.Column(db.String(100))
    posts = db.relationship('Post', backref='venue', lazy=True)

