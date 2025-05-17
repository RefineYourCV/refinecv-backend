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

    @staticmethod
    def update_user_data(user_id:str, update_data: dict) -> dict:
        result = user_schema.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        # Check if document was updated or not found
        if result.matched_count == 0:
            raise ValueError(f"No document found with id {user_id}")
        return True


    @staticmethod
    def update_user_credit(user_id:str, now):
        result = user_schema.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$inc": {"credit": 1},
                    "$set": {"lastCreditAddedAt": now}
                }
        )
        print('result',result)
        return result
    
    @staticmethod
    def decrease_user_credit_safe(user_id: str):
        updated_user = user_schema.find_one_and_update(
            {"_id": ObjectId(user_id), "credit": {"$gt": 0}},
            {"$inc": {"credit": -1}},
            return_document=True  # returns the updated document
        )
        return updated_user

