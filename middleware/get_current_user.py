from fastapi import Depends, Request,HTTPException
import jwt
from core.config import settings

secret_key = settings.SECRET_KEY
private_algo = settings.PRIVATE_JWT_ALGO

def get_curent_user(request:Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, secret_key, algorithms=[private_algo])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")