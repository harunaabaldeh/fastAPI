from fastapi import HTTPException, Response, Depends, status
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import PostSchema
from app.models import Post

class PostService:

    post_not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post was not found")
    
    async def create_post(self, post_in: PostSchema, db_session: Session = Depends(get_db)):
        new_post = Post(**post_in.dict())

        db_session.add(new_post)
        db_session.commit()
        db_session.refresh(new_post)

        return new_post
    
    async def update_post(self, post_id: int, post_in: PostSchema, db_session: Session = Depends(get_db)):
        post = db_session.query(Post).filter(Post.id == post_id).one_or_none()

        if post is None:
            raise self.post_not_found_exception
        
        post.title = post_in.title
        post.content = post_in.content

        db_session.commit()
        db_session.refresh(post)

        return post
    
    async def delete_post(self, post_id: int, db_session: Session = Depends(get_db)):
        post = db_session.query(Post).filter(Post.id == post_id).one_or_none()

        if post is None:
            raise self.post_not_found_exception
        
        db_session.delete(post)
        db_session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    async def get_post(self, post_id: int, db_session: Session = Depends(get_db)):
        post = db_session.query(Post).filter(Post.id == post_id).one_or_none()

        if post is None:
            raise self.post_not_found_exception
        
        return post
    
    async def get_posts(self, db_session: Session = Depends(get_db)):
        return db_session.query(Post).all()
        

post_service = PostService()