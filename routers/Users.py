
from fastapi import APIRouter, status, HTTPException,Depends,Response
from schema import user
from utils.passwords import hash,verify
from utils.JWT import create_tokens,get_current_user
from config import settings
from db.db import users
ACCESS_KEY = settings.access_key
REFRESH_KEY = settings.refresh_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_expire
REFRESH_TOKEN_EXPIRE = settings.refresh_expire

router = APIRouter()
@router.post('/Login',status_code=status.HTTP_200_OK, response_model= user.final_user)
async def login(User:user.base_user,response:Response):
    found = await users.find_one({"email":User.email})
    res = str(found["_id"])
    found["_id"]=res
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Email")

    checkpass = verify(User.password,found["password"])
    if not checkpass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password")    
    data={"_id":found["_id"],"name":found["name"],"email":found["email"]}
    ACCESS_TOKEN=create_tokens(data,ACCESS_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE)
    REFRESH_TOKEN=create_tokens(data,REFRESH_KEY,ALGORITHM,REFRESH_TOKEN_EXPIRE)
    response.set_cookie(key="ACCESS_TOKEN",value=ACCESS_TOKEN,max_age=300000,httponly=True)
    response.set_cookie(key="REFRESH_TOKEN",value=REFRESH_TOKEN,max_age=900000,httponly=True)
    return found 

@router.post('/Signup',status_code=status.HTTP_201_CREATED, response_model= user.final_user)
async def create_user(User:user.in_user):
    found = await users.find_one({"email":User.email})
    if found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already exists")

    password = hash(User.password)
    User.password = password
    doc = User.dict()
    await users.insert_one(doc)
    new = await users.find_one({"email":User.email}) 
    res = str(new["_id"])
    new["_id"]=res
    return new

@router.post('/Logout')
def Logout(response:Response,current_user = Depends(get_current_user)):
    if(current_user):
        response.delete_cookie("ACCESS_TOKEN")
        response.delete_cookie("REFRESH_TOKEN")
        return "deleted cookies"
    else:
        return "cookies do not exist"

@router.get('/Get')
def getUser(current_user = Depends(get_current_user)):
    if(current_user):
        return current_user
        
@router.get('/GetALL')
async def getUser():
    all = []
    cursor = users.find({})
    async for document in cursor:
        id=str(document["_id"])
        document["_id"]=id
        all.append(document)
    return all