from flask import Blueprint,request,render_template,flash,redirect,url_for
from flask_login import login_required, login_user, logout_user
from models import *
import logging as log

auth = Blueprint('auth',__name__)

# LOGIN ROUTES
@auth.route('/login',methods=['GET','POST'])
def login():
  if request.method == "POST":
    user =  User.query.filter_by(email = request.form['email'],password=request.form['password']).first()
    remember = request.form.get('remember')
    if remember :
      remember = True 
    else :
      remember = False
    #if the user cannot be found 
    if not user:
      flash('Login failed !!.. password  or email incorrect')
      # send them to a dedicated page
      log.warning('User authentication faild due to wrong password or email address')
      return redirect(url_for('auth.login'))
    else:
      flash("Hi:  {} {}".format(user.first,user.name))
      login_user(user,remember = remember)
      #print(remember)
      return redirect(url_for('index',user=user))
  return render_template('login.html')  

# LOGIN ROUTES
@auth.route('/signup',methods=['GET','POST'])
def signup():
  if request.method == 'POST':
    user = User(email = request.form['email'],password=request.form['password'])
    # FROM HERE WE HAVE THE AUTHENTICATE AND SEND EMAIL TO USER 
    # TO BE IMPLEMENTED
    db.session.add(user)
    db.session.commit()
    flash(f'Email has been send to {user.email}')
    return redirect(url_for('index'))
  return render_template('signup.html')

# LOGOUT ROUTES
@auth.route('/logout')
@login_required
def log_out():
  logout_user()
  return redirect(url_for('auth.login'))

