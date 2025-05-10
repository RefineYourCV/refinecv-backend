from services.mongodb import db

from bson import ObjectId


history_schema = db["history"] 

class HistoryService:
    
    @staticmethod 
    def save_history(metadata: dict) -> str:
        result = history_schema.insert_one(metadata)
        return str(result.inserted_id)
    
    @staticmethod
    def get_histories(user_id: str):
        return history_schema.find({"userId":user_id}) # Convert cursor to list

    @staticmethod
    def get_history(user_id: str, history_id:str) -> dict:
        obj_id = ObjectId(history_id)
        result = history_schema.find_one({"userId":user_id, "_id":obj_id})
        result["_id"] = str(result["_id"])
        return result