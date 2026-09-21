# class -> table 
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.models.db import Base
from typing import Optional
class UserModel(Base):
    __tablename__="users"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str]= mapped_column(String(100),nullable=False)
    gender:Mapped[str]= mapped_column(String(20), nullable=False)
    email:Mapped[str]= mapped_column(String(255),unique=True,index=True, nullable=False)
    mobile:Mapped[str]= mapped_column(String(255),unique=True,index=True, nullable=False)
    password:Mapped[str]= mapped_column(String(255), nullable=False)
    city:Mapped[Optional[str]]= mapped_column(String(100), nullable=True)
# one to one 
    address:Mapped[Optional["AddressModel"]]= relationship("AddressModel",back_populates="user",uselist=False,cascade="all, delete-orphan")



class AddressModel(Base):
    __tablename__="addresses"
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    street:Mapped[str]=mapped_column(String(255),nullable=False)
    city:Mapped[str]=mapped_column(String(100),nullable=False)
    country:Mapped[str]=mapped_column(String(100),nullable=False)
    pincode:Mapped[int] = mapped_column(nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),unique=True,nullable=False)
    user:Mapped[Optional["UserModel"]]= relationship("UserModel",back_populates="address",uselist=False)
