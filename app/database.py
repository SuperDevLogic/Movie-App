import os
from pymongo import mongo_client
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_CONNECTION_URI = os.environ.get('MONGO_DB_CONNECTION_URI ')

client = mongo_client.MongoClient(MONGO_DB_CONNECTION_URI)
print("Connected to MongoDB")

# Get or create collection
users_collection = client["MOVIE_DB"]["users"]
movies_collection = client["MOVIE_DB"]["movies"]
ratings_collection = client["MOVIE_DB"]["ratings"]
comments_collection = client["MOVIE_DB"]["comments"]
