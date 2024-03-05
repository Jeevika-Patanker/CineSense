from flask import Blueprint,render_template,request,redirect,url_for,flash
from .db_schema import User,Subscription,Payment
from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from .views import views
from flask_login import login_user,logout_user,current_user,login_required

auth  = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
          print(request.form)
          email = request.form.get('email')
          password = request.form.get('password') 
          
          user = User.query.filter_by(email=email).first()
          if user:
                if check_password_hash(user.password,password):
                      flash('Logged in Successfully! Welcome '+user.username,category='success')
                      login_user(user,remember=True)
                      return redirect(url_for('views.movie_home'))
                else:
                      flash('Incorrect password,please try again. ',category='error')     
          else:
                flash('Email id not exist , Register and try again',category='error')     
                
    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
  if request.method == 'POST':
      print(request.form)
      fname = request.form.get('fname')
      uname = request.form.get('uname')
      email = request.form.get('email')
      number = request.form.get('number')
      password = request.form.get('password')
      cpassword = request.form.get('cpassword')
      
      user = User.query.filter_by(email=email).first()
      if user:
            flash('Email Id Already Exists', category='error')
      elif len(fname) < 4:
            flash('name should be greater than 4 characters', category='error')
      elif len(uname) < 4:
            flash('user name should be greater than 4 characters', category='error')
      elif password != cpassword:
            flash('Passwords don\'t match.', category='error')
      elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
      else:
            flash('Choose Subscription Plan', category='success')
            # return redirect(url_for('subscription',email=email,fname=fname,number=number,password=password,uname=uname)) 
            return render_template('subscription.html',fname=fname,uname=uname,email=email,number=number,password=password)     
  return render_template('signup.html')

@auth.route('/subscription',methods=['GET','POST'],)
def subscription():
      if request.method == 'POST':
        print(request.form)
        subs_type = request.form.get('subs_type')
        price = request.form.get('price')
        fname = request.form.get('fname')
        uname = request.form.get('uname')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
   
        if subs_type == '' and price == '':
            flash('Subscription type or price may be null', category='error')     
        else:
            flash('Make Payment', category='success')
            return render_template('payment.html',fname=fname,uname=uname,email=email,number=number,password=password,price=price,subs_type=subs_type)     
      return render_template('subscription.html')
  


@auth.route('/payment',methods=['POST'])
def payment():
    if request.method == 'POST':
        print(request.form)
        subs_type = request.form.get('subs_type')
        price = request.form.get('price')
        fname = request.form.get('fname')
        uname = request.form.get('uname')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
         
        if fname=='':
            flash('Name should be not be null', category='error')
        else:
            new_user = User(fullname=fname,username=uname,email=email,password=generate_password_hash(password),phone_number=number)  
            db.session.add(new_user)
            db.session.commit()
            
            new_subscription = Subscription(subscription_type = subs_type, user=new_user)
            db.session.add(new_subscription)
            db.session.commit()
            
            new_payment = Payment(amount = price , user=new_user, subscription=new_subscription)  
            db.session.add(new_payment)
            db.session.commit()

            flash('Account Created Now Login', category='success')
            return redirect(url_for('auth.login'))         
         

    return render_template('payment.html')

