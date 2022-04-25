from db.db import posts
from db.postmongo import getPosts

async def getAllPosts(id:str):
    list = []
    async for post in posts.find({"user_id":id}):
        list.append(getPosts(post))
    return list

async def getNameAllPosts(name:str):
    list = []
    async for post in posts.find({"user_name":name}):
        list.append(getPosts(post))
    return list
    