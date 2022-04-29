from flask import Flask, flash,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from os import environ
from models import User,Items,Category
from api import api as api_blueprint
from auth import auth as auth_blueprint
from flask_login import LoginManager, login_required
import logging as log

app = Flask(__name__)
load_dotenv('./.env')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_ECHO'] = True
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

log.basicConfig(format='%(asctime)s %(message)s')

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow()
ma.init_app(app)

app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  # since the user_id is just the primary key of our user table, use it in the query for the user
  return User.query.get(int(user_id))

@app.route("/",methods =['GET'])
@login_required
def index():
  key = request.args.get('category',default='1')
  category = Category.query.filter_by(id=key).first()
  categories= Category.query.all()
  items  = Items.query.filter_by(category_id = category.id)
  return render_template('index.html',category = category,categories = categories,items=items)

@app.route("/user/add",methods = ['POST','GET'])
@login_required
def add_user():
  if request.method =="POST":
    # getting the post values from the form
    name= request.form['name']
    first = request.form['first']
    user = User(name=name,first=first)
    # savely add this to the database
    db.session.add(user)
    db.session.commit()
  # this can be get instead if it's a 'GET' request  
  return render_template('add_user.html')



# getting the port from global env
server_port = environ.get('SERVER_PORT')
# ##############################################################
# Starting the application from here with some additional options 
if __name__ == "__main__":
  log.warning('Starting the application')
  app.run(port= server_port)