from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.db import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import User,UserUpdate
from app.models.user_model import UserModel
# get_current_user is the auth dependency: adding it to a handler makes that route
# require a valid "Authorization: Bearer <token>" header (401 otherwise).
from app.core.deps import get_current_user
from pydantic import ValidationError



def _integrity_error_detail(e:IntegrityError) -> str:
    diag = getattr(e.orig, "diag", None)
    if diag is not None and getattr(diag, "message_detail", None):
        return diag.message_detail
    if diag is not None and getattr(diag, "message_primary", None):
        return diag.message_primary
    return str(e.orig) if e.orig is not None else str(e)



# Public route (no get_current_user): anyone can sign up, since a new user has no token yet.
async def create_user(user:User, db:AsyncSession = Depends(get_db)):
    try:
        await UserService.create_user(user, db)
        return {"message":"User created"}
    except ValidationError as e:
        return {"message":"Could not created the user"}
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=_integrity_error_detail(e))



# Protected route: `current_user` is the logged-in user resolved from the token.
async def get_one(id:int, db:AsyncSession = Depends(get_db), current_user:UserModel = Depends(get_current_user)):
    user = await UserService.get_one(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user




async def get_all( db:AsyncSession = Depends(get_db), current_user:UserModel = Depends(get_current_user)):
    users = await UserService.get_all(db)
    return users



async def update_user(id:int, user:UserUpdate, db:AsyncSession = Depends(get_db), current_user:UserModel = Depends(get_current_user)):
    try:
        updated_user = await UserService.update_user(id,user,db)
    except IntegrityError as e:
        raise HTTPException(status_code=409,detail=_integrity_error_detail(e))
    if updated_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return updated_user


async def delete_user(id:int,db:AsyncSession = Depends(get_db), current_user:UserModel = Depends(get_current_user)):
    deleted_user = await UserService.delete_user(id,db)
    if not deleted_user :
        raise HTTPException(status_code=404,detail="User not found")
    return {"message":"User Deleted"}




