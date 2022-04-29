from flask_marshmallow import Marshmallow
from models import *

ma = Marshmallow()

class ItemSchema(ma.SQLAlchemyAutoSchema):

  class Meta:
    model = Items

# ################################################################

item_schema  = ItemSchema()
items_schema = ItemSchema(many=True)