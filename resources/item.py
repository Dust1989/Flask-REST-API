from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3
from models.item import ItemModel
from models.store import StoreModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} is already exists."}, 400

        data = Item.parser.parse_args()

        if StoreModel.find_by_id(data["store_id"]) is None:
            return (
                {"message": f"The store with id {data['store_id']} is not exists."},
                400,
            )

        item = ItemModel(name, **data)

        try:
            ItemModel.save_to_db(item)
        except Exception as e:
            return {"message": f"An error occurred inserting the item.\n {e}"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # 另一种方法
        # return {"items": [item.json() for item in ItemModel.query.all()]}
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}

