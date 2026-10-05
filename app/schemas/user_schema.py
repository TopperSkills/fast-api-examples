from pydantic import BaseModel,Field,EmailStr,field_validator, ValidationError

# pip install 'pydantic[email]'

class Address(BaseModel):
    street:str = ""
    city:str
    country:str
    pincode:int


# ge 
# le 
# min_length 
# max_length 


class User(BaseModel):
    name:str =  Field(min_length=2, max_length=50)
    gender:str 
    email:EmailStr
    mobile:str = Field(pattern=r"^(\+\d{1,3})?[6-9]\d{9}$")
    city:str | None = Field(default=None)
    password:str
    address:Address | None = None


    @field_validator("name")
    @classmethod
    def validate_name(cls,value:str):
        if not all(word.isalpha() for word in value.split()):
            raise ValueError("Name must contains alphabets only")
        else:
            return value.strip().lower()


    @field_validator("name","gender","email","city")
    @classmethod
    def transform_str(cls,value:str):
        if isinstance(value, str):
            return value.strip().lower()


class UserResponse(BaseModel):
    id:int
    name:str
    gender:str
    mobile:str
    email:str
    city:str | None = None
    address:Address | None = None


class AddressUpdate(BaseModel):
    street:str | None = None
    city:str | None = None
    country:str | None = None
    pincode:int | None = None


class UserUpdate(BaseModel):
    name:str | None = Field(default=None, min_length=2, max_length=50)
    gender:str | None = None
    email:EmailStr | None = None
    mobile:str | None = Field(default=None, pattern=r"^(\+\d{1,3})?[6-9]\d{9}$")
    city:str | None = None
    password:str | None = None
    address:AddressUpdate | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls,value:str | None):
        if value is None:
            return value
        if not all(word.isalpha() for word in value.split()):
            raise ValueError("Name must contains alphabets only")
        return value.strip().lower()

    @field_validator("gender","email","city")
    @classmethod
    def transform_str(cls,value:str | None):
        if isinstance(value, str):
            return value.strip().lower()
        return value

