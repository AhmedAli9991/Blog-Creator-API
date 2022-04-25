import os
from fastapi import APIRouter, File, status, HTTPException,Depends, UploadFile
from schema import post
from db.db import posts
from utils.JWT import get_current_user
from utils import qureies
import uuid
from db.postmongo import getPosts
from typing import List,Optional
from bson import ObjectId

router = APIRouter()

@router.post('/add',status_code=status.HTTP_201_CREATED,response_model= post.out_post)
async def add(post:post.base =Depends(),file: UploadFile = File(...),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    FILEPATH = "./db/static/images/"
    file_name = file.filename
    try:
        extension = file_name.split(".")[1]
    finally:
        if extension not in ["png", "jpg", "jpeg","PNG","JPG"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed")
    ab = str(uuid.uuid4())
    img_name = FILEPATH + str(uuid.uuid4()) + "." + extension
    file_content = await file.read()
    with open(img_name, "wb") as f:
        f.write(file_content)
    await posts.insert_one({"Title":post.Title,"desc":post.desc,"photo":img_name,"user_id":current_user["_id"],"user_name":current_user["name"]})
    new1 = await posts.find_one({"Title":post.Title,"desc":post.desc,"photo":img_name,"user_id":current_user["_id"]}) 
    new = getPosts(new1)
    return new
@router.get('/all',status_code=status.HTTP_200_OK,response_model= List[post.out_post])
async def getAll(current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    out = await qureies.getAllPosts(current_user["_id"])
    if(out):
        return out
    else : 
        raise status.HTTP_404_NOT_FOUND

@router.delete('/delete/{id}',status_code=status.HTTP_200_OK,response_model=str)
async def delete(id:str,current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    post = await posts.find_one({"_id": ObjectId(id)})
    if post:
        await posts.delete_one({"_id": ObjectId(id)})
        os.remove(post["photo"])	
        return("deleted")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
@router.get('/one/{id}',status_code=status.HTTP_200_OK,response_model=post.out_post)
async def getOne(id:str,current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    one = await posts.find_one({"_id":ObjectId(id)})
    if one:
        out = getPosts(one)
        return out
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.put('/update/{id}',status_code=status.HTTP_201_CREATED,response_model= post.out_post)
async def update(id:str,post:post.updatemodel =Depends(),file: Optional[UploadFile] = File(None),current_user = Depends(get_current_user)):
    if(current_user==None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    one = await posts.find_one({"_id":ObjectId(id)})
    out = getPosts(one)
    if out:
        if file !=None:
            os.remove(out["photo"])
            FILEPATH = "./db/static/images/"
            file_name = file.filename
            try:
                extension = file_name.split(".")[1]
            finally: 
                if extension not in ["png", "jpg", "jpeg","PNG","JPG"]:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="File extension not allowed")
            ab = str(uuid.uuid4())
            img_name = FILEPATH + str(uuid.uuid4()) + "." + extension
            file_content = await file.read()
            with open(img_name, "wb") as f:
                f.write(file_content)
            await posts.update_one({"_id":ObjectId(id)},{"$set":{"Title":post.Title,"desc":post.desc,"photo":img_name,"user_id":current_user["_id"],"user_name":current_user["name"]}})
            one1 = await posts.find_one({"_id":ObjectId(id)})
            out1 = getPosts(one1)
            return(out1)
            
        else:
            posts.update_one({"_id":ObjectId(id)},{"$set":{"Title":post.Title,"desc":post.desc,"photo":out["photo"],"user_id":current_user["_id"],"user_name":current_user["name"]}})
            one1 = await posts.find_one({"_id":ObjectId(id)})
            out1 = getPosts(one1)
            return(out1)
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
