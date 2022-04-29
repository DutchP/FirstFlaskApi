from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///databases/main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SQLALCHEMY_ECHO'] = True
db= SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  name= db.Column(db.String(25),nullable=False)
  first =db.Column(db.String(25),nullable=False)
  email = db.Column(db.String(120),nullable=False,unique=True)
  password =db.Column(db.String(25),nullable=False)

  def __repr__(self):
    return "<User>: %s"%(self.name)

class Category(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  category = db.Column(db.String,nullable = False)
  item = db.relationship('Items', backref='items', lazy=True)

class Items(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String,nullable=False)
  category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
  price = db.Column(db.Float)

  def to_json(self):
    return {
      'id' : self.id,
      'name' : self.name,
      'category' : self.category_id,
      'price' : self.price
    }
