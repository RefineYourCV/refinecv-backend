from fastapi import APIRouter, Depends
from middleware.get_current_user import get_curent_user
router = APIRouter()


@router.get('/self')
async def get_me(user=Depends(get_curent_user)):
    return user

