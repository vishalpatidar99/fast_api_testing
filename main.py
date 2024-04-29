from fastapi import FastAPI
from app.api.routes.auth_routes import auth_router
from app.api.routes.posts_routes import post_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(post_router)

from app.schemas.models import Post, User
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas.models import User
from app.db.db import get_db

@app.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    posts = db.query(Post).all()
    return users, posts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
