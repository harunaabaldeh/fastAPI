from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session  
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.models import User
from .. import utils


router = APIRouter()

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user_in: UserCreate, db_session: Session = Depends(get_db)):

    hashed_password = utils.get_password_hash(user_in.password)
    user_in.password = hashed_password
    new_user = User(**user_in.model_dump())

    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user

@router.get('/users/{id}', response_model=UserResponse)
async def get_user(id: int, db_session: Session = Depends(get_db)):
    user = await db_session.query(User).filter(User.id == id).one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    return user