from services.mongodb import db
from bson import ObjectId
from bson import ObjectId
from typing import Optional, List

doc_schema = db["documents"] 

class DocManagementService:
    
    @staticmethod 
    def save_document_metadata(metadata: dict) -> str:
        result = doc_schema.insert_one(metadata)
        return str(result.inserted_id)
    
    @staticmethod
    def update_document_metadata(user_id:str, doc_id: str, update_data: dict) -> dict:
        result = doc_schema.update_one(
            {"_id": ObjectId(doc_id),
            "userId": user_id
            },
            {"$set": update_data}
        )
        # Check if document was updated or not found
        if result.matched_count == 0:
            raise ValueError(f"No document found with id {doc_id}")
        return doc_schema.find_one({"_id": ObjectId(doc_id)})
    
    @staticmethod
    def get_user_documents(user_id:str):
        return doc_schema.find({"userId":user_id})

    @staticmethod
    def get_user_document(user_id:str, doc_id:str):
        return doc_schema.find_one({"userId":user_id, "_id":ObjectId(doc_id)})
    
    @staticmethod
    def get_doc_details(user_id:str, doc_id:str, fields: Optional[List[str]] = None) -> dict:
        try:
            projection = {field: 1 for field in fields} if fields else None
            
            details = doc_schema.find_one({"userId":user_id, "_id":ObjectId(doc_id)}, projection)
            
            if not details:
                return {"error": "User not found"}
            
            details["_id"] = str(details["_id"])
            
            return details
        
        except Exception as e:
            return {"error": str(e)}