from fastapi import FastAPI
from app.models import Base
from app.database import engine
from .routers import post, user, auth


Base.metadata.create_all(bind=engine)

api_description = """ Social Media API. You can create posts, read posts, update posts and delete posts. 
                    You can signup, login and logout. 
                    You can also get your user profile. """
app = FastAPI(title='Social Media API', description=api_description, version='1.0.0')


app.include_router(router=post.router, prefix='/api', tags=['posts'])
app.include_router(router=user.router, prefix='/api/auth', tags=['users'])
app.include_router(router=auth.router, prefix='/api/auth', tags=['Auth'])


