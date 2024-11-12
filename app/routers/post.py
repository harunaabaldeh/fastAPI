from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session  
from app.database import get_db
from app.services.post_service import post_service
from app.schemas import PostCreate, Post
from typing import List



router = APIRouter()


@router.get("/posts", response_model=List[Post])
async def get_posts(db_session: Session = Depends(get_db)):
    return await post_service.get_posts(db_session=db_session)

@router.post("/posts", response_model=Post)
async def create_post(post_in: PostCreate, db_session: Session = Depends(get_db)):
    new_post = await post_service.create_post(post_in=post_in, db_session=db_session)
    return new_post

@router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int, db_session: Session = Depends(get_db)):
    post = await post_service.get_post(post_id = post_id, db_session = db_session)
    return post

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db_session: Session = Depends(get_db)):
   return await post_service.delete_post(post_id = post_id, db_session = db_session)


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post_in: PostCreate, db_session: Session = Depends(get_db)):
    db_post = await post_service.update_post(post_id = post_id, post_in = post_in, db_session = db_session)
    return db_post