from app.db import Base, engine
from app.models import User, Post

Base.metadata.create_all(engine)