from fastapi import Depends, Request, HTTPException
import jwt
from core.config import settings
from api.v1.user.user_service import UserService
import datetime

secret_key = settings.SECRET_KEY
private_algo = settings.PRIVATE_JWT_ALGO
user_service = UserService()
def get_curent_user(request:Request):
    auth_header = request.headers.get("Authorization")
 
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, secret_key, algorithms=[private_algo])
        user_id = payload.get("_id")
        user = user_service.get_user_by_id(user_id=user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        last_added = user.get("lastCreditAddedAt", now)

        if last_added.tzinfo is None:
            last_added = last_added.replace(tzinfo=datetime.timezone.utc)
        hours_passed = (now - last_added).total_seconds() / 3600
        if user["credit"] < 3 and hours_passed >= 16:
            user_service.update_user_credit(user_id=user_id, now=now)
            user["credit"] += 1
            user["lastCreditAddedAt"] = now

        user["_id"] = str(user["_id"])
        return user

    except Exception as e:
        print("Error in get_current_user:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")