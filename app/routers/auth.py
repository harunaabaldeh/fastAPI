from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserLogin
from .. import models
from .. import utils
from .. import oauth2


router = APIRouter()


@router.post('/login')
async def login(user_creds:OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    user = await db_session.query(models.User).filter(models.User.email == user_creds.username).one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    valid_password = utils.verify_password(user_creds.password, user.password)

    if not valid_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data = {'user_id': user.id})

    return {'token': access_token, 'token_type': 'bearer'}