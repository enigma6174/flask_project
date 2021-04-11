import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price cannot be empty')

    @classmethod
    def get_item(cls, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,)).fetchone()

        connection.close()

        if result:
            return {'item': {'name': result[0], 'price': result[1]}}

    @classmethod
    def insert_item(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):

        try:
            item = self.get_item(name)
        except Exception as e:
            return {'exception': e}, 500

        if item:
            return item, 200

        return {'message': 'item {} not in database'.format(name)}

    # POST call for the resource - add new item to database
    # Authentication required to modify database
    @jwt_required()
    def post(self, name):

        if self.get_item(name):
            return {'message': 'item {} already exists in database'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert_item(item)
        except Exception as e:
            return {'exception': e}, 500

        return item, 201

    # DELETE call for the resource - delete existing item from database
    # Authentication required to modify database
    @jwt_required()
    def delete(self, name):

        if not self.get_item(name):
            return {'message': 'item {} does not exist'.format(name)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'item {} deleted successfully'.format(name)}

    # PUT call for the resource - update existing item in the database or create new item if not exist
    # Authentication required to modify database
    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = self.get_item(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:

            try:
                self.insert_item(updated_item)
            except Exception as e:
                return {'exception': e}, 500

        else:

            try:
                self.update_item(updated_item)
            except Exception as e:
                return {'exception': e}, 500

        return updated_item, 201


class ItemList(Resource):

    def get(self):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"

        try:
            items = [{'name': result[0], 'price': result[1]} for result in cursor.execute(query)]
        except Exception as e:
            connection.close()
            return {'exception': e}, 500

        connection.close()

        return items, 200
