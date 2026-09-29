# app/services/user_service.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.schemas.user_schema import User,UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import UserModel,AddressModel
from app.core.security import hash_password

# user = {
#     name:"",
#     address:{
#         street:""
#     }
# }
class UserService:
    @staticmethod
    async def create_user(user:User,db:AsyncSession):
        # create Address ORM object 
        address=AddressModel(
            street=user.address.street,
            city=user.address.city,
            country=user.address.country,
            pincode=user.address.pincode,
        )

        # create User ORM object 

        user_model = UserModel(
            name=user.name,
            gender=user.gender,
            email=user.email,
            mobile=user.mobile,
            # Store only the bcrypt hash, never the plain-text password.
            password=hash_password(user.password),
            city=user.city,
            address=address
        )

        db.add(user_model)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise
        await db.refresh(user_model)


    @staticmethod
    async def get_one(
            user_id:int,
            db:AsyncSession
    ):
        result = await db.execute(
            select(UserModel)
            .options(selectinload(UserModel.address))
            .where(UserModel.id ==user_id)
        )

        user = result.scalar_one_or_none()
        return user




    @staticmethod
    async def get_all(
            db:AsyncSession
    ):
        result = await db.execute(
            select(UserModel)
            .options(selectinload(UserModel.address))
        )

        return result.scalars().all()
        

    @staticmethod
    async def update_user(
        user_id:int,
        data:UserUpdate,
        db:AsyncSession
    ):
        result = await db.execute(
            select(UserModel)
            .options(selectinload(UserModel.address))
            .where(UserModel.id ==user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None
        
        update_data = data.model_dump(exclude_unset=True)#client side data
        address_data = update_data.pop("address",None)
        # If the password is being changed, hash the new one before saving.
        if update_data.get("password"):
            update_data["password"] = hash_password(update_data["password"])



        for field, value in update_data.items():
            setattr(user_model,field,value)


        if address_data:
            for field, value in address_data.items():
                setattr(user_model.address,field,value)
        
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise 

        await db.refresh(user_model)
        return user_model
    



    @staticmethod
    async def delete_user(
        user_id:int,
        db:AsyncSession
    ):
        result = await db.execute(
            select(UserModel)
            .where(UserModel.id ==user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return False 
        
        await db.delete(user_model)
        await db.commit()
        return True