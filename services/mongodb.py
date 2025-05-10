from pymongo import MongoClient
from core.config import settings

client = MongoClient(settings.MONGO_URL)

db = client["elevatecv"]