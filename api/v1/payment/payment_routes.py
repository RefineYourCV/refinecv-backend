from fastapi import APIRouter, Depends, HTTPException
from middleware.get_current_user import get_curent_user
from core.config import settings
import requests
router = APIRouter()

Headers = {
    "Accept": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
    "Authorization": f"Bearer {settings.LSQY_API_KEY}"
}

@router.get('/get-product')
async def get_product():
    url = settings.LSQY_ENDPOINT
    try:
        response = requests.get(f"{url}/products", headers=Headers)
        print(response)
        return {"success": True, "data": response.json()}
        
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=str(e))

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")