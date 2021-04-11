from werkzeug.security import safe_str_cmp
from user import User


# Authenticate a username against a password
def authenticate(username, password):

    user = User.find_username(username)

    if user and safe_str_cmp(user.password, password):
        return user


# Identity(payload) - Unique to Flask-JWT where `payload` is contents of JWT token
# Extract userid from payload and retrieve the specific user that matches payload
def identity(payload):
    user_id = payload['identity']
    return User.find_userid(user_id)
