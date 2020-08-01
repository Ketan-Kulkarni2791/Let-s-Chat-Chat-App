from pymongo import MongoClient
from werkzeug.security import generate_password_hash

from user import User

# client = MongoClient("mongodb+srv://test:test@lets-chat.ndh21.mongodb.net/ChatDB?retryWrites=true&w=majority")

# Let's get the database to connect to it.
# chat_db = client.get_database("ChatDB")
# Let's get the collection in it.
# users_collection = chat_db.get_collection("users")


# Let's save the user to our database
# def save_user(username, email, password):
#     password_hash = generate_password_hash(password)
#     # insert_one({}) is the function where you pass data in the form of dictionary.
#     # Any key in the dictionary starts with '_' is considered as primary key. Username is our primary key.
#     users_collection.insert_one({"_id": username, "email": email, "password": password_hash})
#
#
# def get_user(username):
#     user_data = users_collection.find_one({"_id" : username})
#     return User(user_data['username'], user_data['email'], user_data['password']) if user_data else None
