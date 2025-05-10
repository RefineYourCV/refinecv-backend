from fastapi import APIRouter, Depends
from middleware.get_current_user import get_curent_user
from .history_service import HistoryService
from core.utils import serialize_mongo_document
router = APIRouter()
history_service = HistoryService()



@router.get("/all")
def get_all_history(user=Depends(get_curent_user)):
    user_id = user["_id"]
    cursor = history_service.get_histories(user_id=user_id)
    histories = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
        histories.append(doc)
    return {"histories":histories}
    

@router.get("/get/{history_id}")
def get_all_history(history_id:str,user=Depends(get_curent_user)):
    user_id = user["_id"]
    history = history_service.get_history(user_id=user_id,history_id=history_id)
    return {"history":history}