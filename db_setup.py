from app.db.db import Base, engine
from app.schemas.models import User, Post

Base.metadata.create_all(engine)