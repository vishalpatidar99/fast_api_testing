from fastapi import HTTPException
from app.schemas.models import User,Post
from app.schemas.schemas import PostCreate
from uuid import uuid4
from app.db.db import get_db

class PostHandler:

    def add_post(self, post: Post, current_user: User):
        # Validate payload size
        if len(post.text.encode('utf-8')) > 1024 * 1024:  # 1 MB limit
            raise HTTPException(status_code=400, detail="Payload size exceeds 1 MB")
        new_post = Post(text=post.text, user_id=post.user_id)
        db = next(get_db())
        db.add(new_post)
        db.commit()  # Commit the transaction to save the post to the database
        
        db.refresh(new_post) # Refresh the post instance to ensure it contains any changes made by the database
        return new_post.id
    



    def get_posts(self, current_user: User):
        db = next(get_db())  # Assuming get_db() returns a generator
        # Retrieve the email from the current user's sub
        user_email = current_user['sub']

        # Query the database to find the user by email
        user = db.query(User).filter(User.email == user_email).first()      
        if user is None:   # Check if the user exists
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user.id
        posts = db.query(Post).filter(Post.user_id == user_id).all()
        # Convert the Post objects to dictionaries
        user_posts = [{"text": post.text, "id": post.id, "user_id": user_id} for post in posts]
        return user_posts


    def delete_post(self, post_id: int, current_user: User):   # getting error in thesew code 
            # Get the database session
            db = next(get_db())
            # Get the post from the database by its id
            post = db.query(Post).get(post_id)

            # Check if the post exists
            if post is None:
                raise HTTPException(status_code=404, detail="Post not found")
            user_email = current_user['sub']
            user = db.query(User).filter(User.email == user_email).first()   

            # Check if the post belongs to the current user
            if post.user_id != user.id:
                raise HTTPException(status_code=403, detail="You are not allowed to delete this post")

            # Delete the post from the database
            db.delete(post)
            db.commit()