from flask import Blueprint,render_template,request,redirect,flash,jsonify
from flask_login import current_user,login_required
import os
import joblib
import  pandas as pd
from . import db
from .db_schema import Review,User,Subscription
from .movie_recommendations import get_recommendations,get_top_10_movie_ids,get_popular_movies,get_movie_details
import json

views  = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('movie_home')
@login_required
def movie_home():
  
    user_id = current_user.id
    
    # Query reviews with rating above 5 for a specific user
    reviews_above_5 = Review.query.filter((Review.rating >= 5) & (Review.user_id == user_id) & (Review.label == True)).limit(8).all()
    
    # Extract unique movie IDs
    movie_ids_above_5 = list(set(review.movie_id for review in reviews_above_5))
    
    print(movie_ids_above_5)
    
    api_key = 'b2084cac0164f1d1fb47762399c270af'
    recommended_movies = get_recommendations(movie_ids_above_5, api_key)
    top_10_movie_ids = get_top_10_movie_ids(recommended_movies)

    # If no recommended movies, get popular movies
    if not top_10_movie_ids:
        top_10_movie_ids = get_popular_movies(api_key)

    movie_details = []

    for movie_id in top_10_movie_ids:
        movie_details.append(get_movie_details(movie_id, api_key))
        
    return render_template('movie_home.html',recommended_movies=movie_details)


@views.route('current_screen',methods=['GET'])
@login_required
def current_screen():
    
    type=request.args.get('type')
    movieid=request.args.get('movieId')
    
    reviews = Review.query.filter_by(movie_id=movieid).order_by(Review.timestamp.desc()).all()

    
    for review in reviews:
      print(f'reviewid: {review.id}, userid: {review.user_id}, {review.movie_id} ,{review.user.username}, {review.rating},{review.review},{review.label}')
    
    return render_template('current_screen.html',type = type, movieid=movieid ,reviews=reviews)
           

@views.route('/predict',methods=['POST'])
def predict():
    if request.method=='POST':
        print(request.form)
        
        movieId= request.form.get('movieId')
        type= request.form.get('type')
        userId = current_user.id
        rating = request.form.get('rating') 
        comment =request.form.get('comment')
        print(comment)
        review = pd.Series(comment)
        print(comment)
        label = predict_classes(review)
        
        print(f'user id :{userId}, movie id : {movieId} , rating : {rating} , review : {comment} , label : {label} ')
        try:
        # Create a new review instance
          new_review = Review(user_id=userId,movie_id=movieId,rating=rating,review=comment,label=label) 
        # Add the review to the session
          db.session.add(new_review)
        # Commit the changes to the database
          db.session.commit()
         
          flash('successfully added review',category='success')
          return redirect(f'current_screen?movieId={movieId}&type={type}')
    
        except Exception as e:
            # An error occurred, rollback the session
            db.session.rollback()
            print(f"Error: {e}")
            flash('Getting Error in adding review check console',category='error')
            return redirect(f'current_screen?movieId={movieId}&type={type}')

        finally:
          # Close the session
           db.session.close()
                   


def predict_classes(review):
    model_path= os.getcwd()+r'\models\model'
    cleaning = joblib.load(model_path+r'\data_cleaner.pkl')
    vector = joblib.load(model_path+r'\tfidf_vector.pkl')
    classifer = joblib.load(model_path+r'\classifier.pkl')
    
    review = cleaning.transform(review)
    review=vector.transform(review)
    prediction= classifer.predict(review)
    
    return prediction[0]
  
  
@views.route('explore',methods=['GET'])
@login_required
def explore():
    
    type=request.args.get('type')
    
    return render_template('explore.html',type = type) 
  
@views.route('user_info',methods=['GET'])
@login_required
def user_info():
    user_id = current_user.id
    
    # Query reviews with rating above 5 for a specific user
    my_reviews = Review.query.filter((Review.user_id == user_id)).all()
    user = User.query.get(user_id)
    subscription = (Subscription.query
                    .filter((Subscription.user_id == user_id))
                    .order_by(Subscription.subscription_date.desc())
                    .first())
    
    if user_id and user.payments:
      latest_payment = user.payments[-1]
      amount = latest_payment.amount
      print(amount)
      
    for review in my_reviews:
      print(f'reviewid: {review.id}, userid: {review.user_id}, {review.movie_id} ,{review.user.username}, {review.rating},{review.review},{review.label}')
    
    return render_template('user_info.html',reviews=my_reviews ,user = user,subscription = subscription,amount=amount)   
  
@views.route('deleteReview',methods=['POST'])
def deleteReview():
  review  = json.loads(request.data)
  reviewId=review['reviewId']
  review = Review.query.get(reviewId)
    # Perform your delete operation based on the reviewId
  if review:
      if review.user_id == current_user.id:
         db.session.delete(review)
         db.session.commit()
  
  return jsonify({})
