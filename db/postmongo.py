def getPosts(post) -> dict:
    return{
        "id": str(post["_id"]),
        "Title":post["Title"],
        "desc" : post["desc"],
        "user_id": post["user_id"],
        "user_name":post["user_name"],
        "photo" : post["photo"]
    }
