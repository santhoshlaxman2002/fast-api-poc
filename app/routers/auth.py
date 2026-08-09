from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import get_auth_service
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login")
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service)
):
    user = service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    access_token = service.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}