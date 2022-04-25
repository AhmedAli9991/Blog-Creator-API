from ast import alias

from pydantic import BaseModel, EmailStr,Field
class base_user(BaseModel):
    email : EmailStr
    password : str

class in_user(base_user):
    name: str

class final_user(in_user):
    id : str= Field(alias="_id")    
