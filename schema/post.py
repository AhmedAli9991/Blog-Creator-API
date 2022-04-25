from pydantic import BaseModel,Field

from typing import Optional
class base(BaseModel):
    Title : str
    desc : str
        
class out_post(base):
    user_id : Optional[str]
    user_name:Optional[str]
    photo : str
    id : str= Field(alias="_id")
    class Config:
        allow_population_by_field_name = True
class updatemodel(BaseModel):
    Title :Optional[str]
    desc : Optional[str]
        