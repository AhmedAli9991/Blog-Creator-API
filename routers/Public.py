from fastapi import APIRouter,status, HTTPException
from db.db import posts
from typing import List
from utils import qureies
from db.postmongo import getPosts
from schema import post
from bson import ObjectId
router = APIRouter()

@router.get('/all/{name}',status_code=status.HTTP_200_OK,response_model= List[post.out_post])
async def getAll(name:str):
    out =await qureies.getNameAllPosts(name)
    if out:
        return out
    else : 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
@router.get('/one/{id}',status_code=status.HTTP_200_OK,response_model=post.out_post)
async def getOne(id:str):
    one = await posts.find_one({"_id":ObjectId(id)})
    if one:
        out = getPosts(one)
        return out
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)