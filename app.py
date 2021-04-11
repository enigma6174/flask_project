from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from user import RegisterUser
from item import Item, ItemList
from security import authenticate, identity

# Flask object
app = Flask(__name__)

# JWT secret key
app.secret_key = 'secret2021'

# Api object
api = Api(app)

# JWT object for authentication
# Creates a new endpoint /auth where we make a request with username and password in JSON body
# The JSON body is verified with authenticate(username, password) and a JWT token is generated
# JWT calls identity(payload) with the token and from it extracts the userid to get the correct username
# Correct username from the extracted userid of the JWT token means the token was valid and authentication success
jwt = JWT(app, authenticate, identity)


api.add_resource(RegisterUser, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
