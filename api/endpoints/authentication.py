from datetime import timedelta
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api import models
from api.schemas import tokens as schemas_tokens
from api.crud import auth as crud_auth
from api.database import get_db

router = APIRouter()


@router.post("/token", response_model=schemas_tokens.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud_auth.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud_auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud_auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
    current_user: models.User = Depends(crud_auth.get_current_active_user),
):
    return current_user
