from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    first = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        """Representoin of the class"""
        return "<User %d>: %s" % (self.id,self.name)

    def to_json(self):
        """Returning a Json string """
        return {
            'id': self.id,
            'first': self.first,
            'name': self.name,
            'email': self.email,
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    item = db.relationship('Items', backref='items', lazy=True)

    def __repr__(self):
        """Represention of the class"""
        return f"<Category {self.id}> , {self.category}"

    def to_json(self):
        return {'category': self.category}


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    price = db.Column(db.Float)

    def __repr__(self):
        """"Representation of the class"""
        return f"<Item {self.id}>: {self.name} {self.price}  <Category {self.category_id}> {Category.category}"

    def to_json(self):
        """returning a json sting"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category_id,
            'price': self.price
        }

    def __str__(self):
        """" A String representation of the class"""
        return f"<Item {self.id}>: {self.name} {self.price}  <Category {self.category_id}> {Category.category}"
