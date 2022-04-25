from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import Users
from routers import Posts
from routers import Public
from db.db import users

app = FastAPI(
    title="Blog creator",
    description="This is a blog creation app where user can register and make a blog and others can visit that blog also uses allows user to upload images ",
    contact={
        "name": "Ahmed Ali",
        "email": "ahmedalibalti2000@gmail.com"
        })

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Public.router, prefix="/Visitor",tags=["Visitor"])
app.include_router(Posts.router, prefix="/User/Posts",tags=["Blog Owner"])
app.include_router(Users.router, prefix="/User",tags=["Users"])


