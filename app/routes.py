from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session  
from app.database import get_db
from app.services import post_service
from app.schemas import PostSchema

router = APIRouter()


@router.get("/posts")
async def get_posts(db_session: Session = Depends(get_db)):
    posts = await post_service.get_posts(db_session=db_session)
    return {'posts': posts}

@router.post("/posts")
async def create_post(post_in: PostSchema, db_session: Session = Depends(get_db)):
    new_post = await post_service.create_post(post_in=post_in, db_session=db_session)
    return {'post': new_post}

@router.get("/posts/{post_id}")
async def get_post(post_id: int, db_session: Session = Depends(get_db)):
    post = await post_service.get_post(post_id = post_id, db_session = db_session)
    return {'post': post}

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db_session: Session = Depends(get_db)):
    await post_service.delete_post(post_id = post_id, db_session = db_session)


@router.put("/posts/{post_id}")
async def update_post(post_id: int, post_in: PostSchema, db_session: Session = Depends(get_db)):
    db_post = await post_service.update_post(post_id = post_id, post_in = post_in, db_session = db_session)
    return {'post': db_post}