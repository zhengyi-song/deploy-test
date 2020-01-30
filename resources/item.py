from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required = True,
                        help = 'This field cannot be left blank!'
                       )
    parser.add_argument('store_id',
                        type = int,
                        required = True,
                        help = 'Every item needs a store_id!'
                       )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found.'}
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
            #print(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500
        item = ItemModel(name, **data)#don't know why after saving, item disappear
        #print(item.name,item.price)
        return item.json(), 201
    
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item {} is deleted'.format(name)}
    
    def put(self,name):
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name,**data)
        item.save_to_db()
        item = ItemModel(name,**data)# the same here as the post
        return item.json()         
    
class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
    
    