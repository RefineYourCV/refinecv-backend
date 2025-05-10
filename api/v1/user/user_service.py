from services.mongodb import db
from bson import ObjectId


user_schema = db["users"] 

class UserService:


    @staticmethod 
    def create_user(user_data: dict) -> str:
        result = user_schema.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def get_user_by_email(email: str) -> dict | None: 
        clean_email = email.strip()
        user = user_schema.find_one({"email": clean_email})
        return user 

    @staticmethod
    def get_user_by_id(user_id: str) -> dict | None:
        try:
            obj_id = ObjectId(user_id)
            user = user_schema.find_one({"_id": obj_id})
            return user
        except Exception as e:
            print(f"Error finding user by ID {user_id}: {e}")
            return None
