from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.Integer)  
    payments = db.relationship('Payment', backref='user')
    subscriptions = db.relationship('Subscription', backref='user_subscriptions')
    user_reviews = db.relationship('Review', backref='user_reviews')

    
class Payment(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime(timezone=True), nullable=False,default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False,unique=True)

    subscription = db.relationship('Subscription', cascade='all, delete-orphan', single_parent=True)
    
    
class Subscription(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    subscription_type = db.Column(db.String(50), nullable=False)
    subscription_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Define the relationship with User
    payment = db.relationship('Payment', backref='subscription_relation_to_payments')
    user = db.relationship('User', backref='subscription', cascade='all, delete-orphan', single_parent=True)


    
    
class Review(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    review = db.Column(db.String(500))
    label = db.Column(db.Boolean, nullable=False)
    user = db.relationship('User', backref='users_relation_to_reviews')



    
