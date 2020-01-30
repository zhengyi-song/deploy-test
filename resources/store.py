from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message':'store is not found'}
    
    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'store {} has already existed'.format(name)}
        store = StoreModel(name)
        store.save_to_db()
        store = StoreModel(name)
        
        return store.json()
                    
                    
    
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()
        
        return {'message':'store is deleted'}

class StoreList(Resource):
    def get(self):
        return {'store':[store.json() for store in StoreModel.query.all()]}