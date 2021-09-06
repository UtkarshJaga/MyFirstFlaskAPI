from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This Field Cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Every Item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting item"}, 500   # Internal server error

        return {"message": "Item {0} Created with price {1}.".format(name, data['price'])}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_to_db()
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            #
            # query = "DELETE FROM items where name=?"
            # cursor.execute(query, (name,))
            # connection.commit()
            # connection.close()
            return {'Message': 'Item Deleted'}
        else:
            return {'Message': 'Item does not exists'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])   # item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        # items = []
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # rows = cursor.execute(query)
        # for row in rows:
        #     items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        #
        # connection.commit()
        # connection.close()
        return {'items': [item.json() for item in ItemModel.query.all()]}


