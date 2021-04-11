import sqlite3
from flask_restful import Resource, reqparse


# Class to create user object with 3 attributes - userid, username, password
class User:

    # Initialize user object with user data
    def __init__(self, uid, _username, _password):
        self.id = uid
        self.username = _username
        self.password = _password

    # Find the userdata mapped to the username supplied by client in the database
    @classmethod
    def find_username(cls, username):

        # Connect to the specified database
        connection = sqlite3.connect('data.db')

        # Initialize cursor
        cursor = connection.cursor()

        # Query to select specified username from table
        query = "SELECT * from users WHERE username=?"

        # Execute and store the result of query
        result = cursor.execute(query, (username,))

        # Fetch first record from result
        row = result.fetchone()

        # If the row has data, initialize the class User with the row data
        if row:
            user = cls(*row)
        else:
            user = None

        # Release the resource - connection close
        connection.close()

        return user

    # Find the userdata mapped to the userid supplied by client in the database
    @classmethod
    def find_userid(cls, uid):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from users where id=?"

        result = cursor.execute(query, (uid,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()

        return user


# Class that provides a Flask resource to register the users
class RegisterUser(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True, help='Username cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')

    def post(self):

        data = RegisterUser.parser.parse_args()

        if User.find_username(data['username']):
            return {"message": "user {} already exists".format(data['username'])}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully"}, 201
