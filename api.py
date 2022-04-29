from flask import Blueprint,jsonify,request
from models import *
from schemas import items_schema,item_schema

api = Blueprint('api',__name__)

# ##################################################################
# API routes for category
# GET reqeust to get all the categories
@api.route('/api/category',methods=['GET'])
def categories():
  categories = Category.query.all()
  cat_list=[]
  for cat in categories:
    cat_list.append({'category_id':cat.id,'category':cat.category})    
  return jsonify(cat_list)

# GET reqeust to get one of the categories based on it's id
@api.route('/api/category/<id>',methods=['GET'])
def category(id):
  category = Category.query.get(id)
  return jsonify({"category_id":category.id,"category":category.category})

# POST request to create a category new record
@api.route('/api/category',methods=['POST'])
def add_category():
  category = request.json['category']
  new_category = Category(category=category)
  db.session.add(new_category)
  db.session.commit()
  return jsonify({'status':'OK','category_id':new_category.id})

# PUT request to update a category record
@api.route('/api/category/<id>',methods=['PUT']) 
def update_category(id):
  old_category = Category.query.get(id)
  category = request.json['category']
  old_category.category=category
  db.session.commit()
  return jsonify({'status':'OK',"category_id":old_category.id,"category":old_category.category})

# Delete request to delete a category record
@api.route('/api/category/<id>',methods=['DELETE'])
def delete_category(id):
  old_category = Category.query.get(id)
  db.session.delete(old_category)
  db.session.commit()
  return jsonify({'status':'OK',"messagge":"Category deleted"})

# GET request to select all items
@api.route('/api/item' , methods=['GET'])
def get_items():
  items = Items.query.all()
  return jsonify(items_schema.dump(items))

# GET request for 1 item 
@api.route('/api/item/<id>',methods=['GET'])
def get_item(id):
  try:
    item = Items.query.get(id)
    category = Category.query.get(item.category_id)
  except AttributeError as e:
    return jsonify(message=" Sorry, Key does not exist"),206
  return jsonify(item_schema.dump(item))

# POST request to add an item
@api.route('/api/item',methods=['POST'])
def add_item():
  item = Items(name=request.json['name'],category_id=request.json['category_id'],price=request.json['price'])
  db.session.add(item)
  db.session.commit()
  return jsonify(message="Item add to database"),200

# PUT reqeust to update an item
@api.route('/api/item/<id>',methods=['PUT'])
def update_item(id):
  try:
    item = Items.query.get(id)
  except AttributeError as e:
    return jsonify(message="Oops something went wrong".e),404
  else:
    item.name = request.json['name']
    item.category_id = request.json['category_id']
    item.price = request.json['price']
    db.session.commit()
    return jsonify(message="Item succesfully updated"),200

# DELETE reqeust to update an item 
@api.route('/api/item/<id>',methods=['DELETE'])
def delete_item(id):
  item = Items.query.get(id)
  db.session.delete(item) 
  return jsonify(message = "Item deleted from the database")
