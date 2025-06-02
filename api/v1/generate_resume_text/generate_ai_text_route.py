from fastapi import APIRouter, Depends
from middleware.get_current_user import get_curent_user
from api.v1.doc_management.doc_management_service import DocManagementService
from services.AI_service import AIService
from core.utils import clean_json_output
from pydantic import BaseModel
import datetime
from ..history.history_service import HistoryService
from ..user.user_service import UserService

router = APIRouter()
ai_service = AIService()
history_service = HistoryService()

doc_management = DocManagementService()
user_service = UserService()

@router.get("/summarize/{doc_id}")
def summarize_resume(doc_id: str,user=Depends(get_curent_user)):
    user_id = user["_id"]
    result = doc_management.get_user_document(user_id=user_id, doc_id=doc_id)

    if "ai_summary" in result:
        cleaned = result["ai_summary"]

        return {"summary":cleaned}
    else:
        user_prompt = result["content"]
        summarize_system_prompt = ""
        with open("prompts/summarize_system_prompt.txt","r",encoding="utf-8") as f:
            summarize_system_prompt = f.read()
        
        summary = ai_service.invoke(user_prompt=user_prompt, system_prompt=summarize_system_prompt)
        cleaned = clean_json_output(summary)
        data_to_be_save = {
            "ai_summary":cleaned
        }

        doc_management.update_document_metadata(user_id=user_id, doc_id=doc_id, update_data=data_to_be_save)

        return {"summary":cleaned}
    

class UpdateFileMetadata(BaseModel):
    jd:str

@router.post("/jd-feedack/{doc_id}")
def jd_feedack(body:UpdateFileMetadata,doc_id: str,user=Depends(get_curent_user)):
    jd = body.jd
    user_id = user["_id"]
    user = user_service.get_user_by_id(user_id=user_id)
    
    if(user["credit"] == 0):
        return {"error":"No credit left. Please retry after 16 hours"}
    
    content = doc_management.get_doc_details(user_id=user_id, doc_id=doc_id,fields=["content"])
    
    feedback_system_prompt = ""
    with open("prompts/feedback_system_prompt2.txt","r",encoding="utf-8") as f:
        feedback_system_prompt = f.read()
        
    feedback_system_prompt = feedback_system_prompt.replace("{{RESUME}}", content["content"])
    user_prompt = f"""
    Here is a job description for a role the user wants to apply to:
    {jd}
    """
    print('feedback_system_prompt',feedback_system_prompt)
    print('user_prompt',user_prompt)
    summary = ai_service.invoke(user_prompt=user_prompt, system_prompt=feedback_system_prompt)
    print("summary",summary)
    cleaned = clean_json_output(summary)
    save_metadata = {
            "document_id":content["_id"], 
            "userId":user_id,
            "content":content['content'],
            "feedback":cleaned,
            "createdAt": datetime.datetime.now(tz=datetime.timezone.utc),
            "updatedAt": datetime.datetime.now(tz=datetime.timezone.utc),   
            "jd":jd
    }
    history_service.save_history(metadata=save_metadata)
    user_service.decrease_user_credit_safe(user_id=user_id)
    return {"feedback":cleaned}



@router.post("/clean-jd")
def clean_jd(body:UpdateFileMetadata):
    jd = body.jd

    clean_system_prompt = ""
    with open("prompts/clean_jd_system_prompt.txt","r",encoding="utf-8") as f:
        clean_system_prompt = f.read()
        
    clean_system_prompt = clean_system_prompt.replace("{{RAW_HTML_CONTENT}}", jd)

    clean_html = ai_service.invoke(user_prompt="clean this html formatted job description", system_prompt=clean_system_prompt)

    return {"clean_data":clean_html}