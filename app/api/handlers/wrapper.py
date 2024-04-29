from app.api.handlers.auth_handlers import UserHandler
from app.api.handlers.post_handlers import PostHandler

USER = None
def get_user_handler():
    global USER

    if USER is None:
        USER = UserHandler()
    
    return USER