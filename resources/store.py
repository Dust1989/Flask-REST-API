from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name} is already exists."}, 400

        store = StoreModel(name)

        try:
            StoreModel.save_to_db(store)
        except Exception as e:
            return {"message": f"An error occurred inserting the store.\n {e}"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"message": "store deleted"}


class StoreList(Resource):
    def get(self):
        # 另一种方法
        # return {"stores": [store.json() for store in StoreModel.query.all()]}
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}

