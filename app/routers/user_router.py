from fastapi import APIRouter
from app.schemas.user_schema import UserResponse
from app.handlers.user_handler import create_user,get_one,get_all,update_user,delete_user
router = APIRouter(prefix="/users",tags=["Users"])
# @router.get("/{id}")
# def get_user(id:int):
#     get_one(id)





router.post("/")(create_user)
router.get("/{id}",response_model=UserResponse)(get_one)
router.get("/",response_model=list[UserResponse])(get_all)
router.put("/{id}",response_model=UserResponse)(update_user)
router.delete("/{id}")(delete_user)

