from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
import os
router = APIRouter()
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import jwt  # PyJWT
import datetime
from .user_service import UserService
from core.config import settings


# config
config = Config('.env')
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET')
SECRET_KEY = config('SECRET_KEY')




# Setup OAUTH
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


def create_jwt(user_info):
    if "_id" in user_info:
        user_info["_id"] = str(user_info["_id"])
        
    payload = {
        **user_info,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


@router.get('/auth/google')
async def login(request:Request):
    redirect_uri = f"{settings.BACKEND_URL}/v1/user/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/auth/google/callback')
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    userinfo = token['userinfo']

    user_details = {
        "email":userinfo["email"].strip(),
        "name": userinfo["name"].strip(),
        "picture":userinfo["picture"].strip(),
        "provider":"google",
        "createdAt": datetime.datetime.now(tz=datetime.timezone.utc),
        "updatedAt": datetime.datetime.now(tz=datetime.timezone.utc),
        "credit":3,
        "subscription":"Freemium",
        "dailyCredit":1,
        "lastCreditAddedAt": datetime.datetime.now(tz=datetime.timezone.utc)
    }
    
    existing_user = UserService.get_user_by_email(userinfo["email"])
    if existing_user:
        print("found")
        user_details = existing_user
    else:
      print("not found")
      inserted_id = UserService.create_user(user_data=user_details)
      user_details = {**user_details, "_id": inserted_id}
    
    
    
    print("user_details",user_details)
    
    # Generate JWT for your app
    app_jwt = create_jwt(user_details)
    print(app_jwt)
    
    # For Chrome Extension → redirect with token in query
    extension_redirect = f'{settings.EXTENSION_URL}/callback?token=Bearer {app_jwt}'
    return RedirectResponse(url=extension_redirect)