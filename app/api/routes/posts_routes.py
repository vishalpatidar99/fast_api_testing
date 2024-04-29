from fastapi import APIRouter, Depends, HTTPException
from app.schemas.models import User
from app.schemas.schemas import PostCreate, Post
from app.api.handlers.post_handlers import PostHandler
from app.utils.auth import verify_token

post_router = APIRouter()
post_handler = PostHandler()

@post_router.post("/addpost/", response_model=str)
async def add_post(post: Post, current_user: User = Depends(verify_token)):
    try:
        post_id = post_handler.add_post(post, current_user)
        return post_id
    except HTTPException as e:
        raise e

@post_router.get("/getposts/", response_model=list[Post])
async def get_posts(current_user: User = Depends(verify_token)):
    # print(current_user)
    try:
        posts = post_handler.get_posts(current_user)
        return posts
    except HTTPException as e:
        raise e




@post_router.delete("/deletepost/{post_id}/")
async def delete_post(post_id: int, current_user: User = Depends(verify_token)):
    try:
        post_handler.delete_post(post_id, current_user)
        return {"message": "Post deleted successfully"}
    except HTTPException as e:
        raise e

