from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.db import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import User,UserUpdate
from pydantic import ValidationError



def _integrity_error_detail(e:IntegrityError) -> str:
    diag = getattr(e.orig, "diag", None)
    if diag is not None and getattr(diag, "message_detail", None):
        return diag.message_detail
    if diag is not None and getattr(diag, "message_primary", None):
        return diag.message_primary
    return str(e.orig) if e.orig is not None else str(e)



async def create_user(user:User, db:AsyncSession = Depends(get_db)):
    try:
        await UserService.create_user(user, db)
        return {"message":"User created"}
    except ValidationError as e:
        return {"message":"Could not created the user"}
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=_integrity_error_detail(e))



async def get_one(id:int, db:AsyncSession = Depends(get_db)):
    user = await UserService.get_one(id, db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user




async def get_all( db:AsyncSession = Depends(get_db)):
    users = await UserService.get_all(db)
    return users



async def update_user(id:int, user:UserUpdate, db:AsyncSession = Depends(get_db)):
    try:
        updated_user = await UserService.update_user(id,user,db)
    except IntegrityError as e:
        raise HTTPException(status_code=409,detail=_integrity_error_detail(e))
    if updated_user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return updated_user


async def delete_user(id:int,db:AsyncSession = Depends(get_db)):
    deleted_user = await UserService.delete_user(id,db)
    if not deleted_user :
        raise HTTPException(status_code=404,detail="User not found")
    return {"message":"User Deleted"}




