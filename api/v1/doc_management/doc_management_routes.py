from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel
from middleware.get_current_user import get_curent_user
from services.S3Storage import S3Storage
from core.constant import max_file_size
from .doc_management_service import DocManagementService
import datetime
from .extract_text import read_pdf_from_url

router = APIRouter()
storage = S3Storage()
doc_management = DocManagementService()

class FileMetadata(BaseModel):
    contentType: str
    fileName: str
    size: int
    slug:str



    
@router.post('/generate-upload-url')
async def generate_upload_url(metadata:FileMetadata,user=Depends(get_curent_user)):
    if metadata.size > max_file_size:
        raise HTTPException(status_code=413, detail="File too large")
        
    user_id = user['_id']
    url = storage.put_object(
            user_id=user_id,
            content_type=metadata.contentType,
            file_name=metadata.slug
    )
    if url:
        save_metadata = {
            **metadata.dict(), 
            "createdAt": datetime.datetime.now(tz=datetime.timezone.utc),
            "updatedAt": datetime.datetime.now(tz=datetime.timezone.utc),
            "status":"pending",
            "userId":user_id
        }
        doc_id = doc_management.save_document_metadata(save_metadata)
        
        return {"url":url, "document_id":doc_id}
    else:
        raise HTTPException(status_code=500, detail="Somthing went wrong")
    
    
    
class UpdateFileMetadata(BaseModel):
    docId:str
    status:str
    fileName:str
    slug:str
    

def serialize_mongo_document(doc):
    return {**doc, "_id": str(doc["_id"])}

@router.post('/update-document')
async def update_document(metadata: UpdateFileMetadata, user=Depends(get_curent_user)):
    user_id = user["_id"]
    doc_id = metadata.docId 
    file_name = metadata.fileName
    slug = metadata.slug
    
    content_type = file_name.split('.')[1]
    
    file_path = f"user-uploads/{user_id}/{slug}.{content_type}"
    
    fileUrl = storage.get_object_url(file_name=file_path)
    
    content = read_pdf_from_url(signed_url=fileUrl, filetype=content_type)
    
    
    
    save_metadata = {
        **metadata.dict(exclude={"docId","fileName","slug"}), 
        "content":content,
        "updatedAt": datetime.datetime.now(tz=datetime.timezone.utc)
    }

    result = doc_management.update_document_metadata(
        user_id=user_id,
        doc_id=doc_id,
        update_data=save_metadata
    )
    
    return {"doc": serialize_mongo_document(result)}


@router.get('/get_data')
async def user_document(user=Depends(get_curent_user)):
    user_id = user["_id"]
    result = doc_management.get_user_documents(user_id=user_id)
      # Convert cursor to list and map ObjectId to str
    docs = []
    for doc in result:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
        docs.append(doc)
    return {'doc': docs}
