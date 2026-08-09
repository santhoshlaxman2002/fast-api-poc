import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import oauth2_scheme
from app.core.settings import settings
from app.models.user import User
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.exceptions import InvalidTokenException, InvalidAuthenticationCredentialsException, UserNotFoundException

def get_auth_service() -> AuthService:
    repository = UserRepository()
    return AuthService(repository)

def get_token(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ]
):
    return token

def decode_token(
    token: Annotated[
        str,
        Depends(get_token)
    ]
):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except InvalidTokenError:
        raise InvalidTokenException()

def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme)
    ],
    db: Session = Depends(get_db)
):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidAuthenticationCredentialsException()
    user = db.get(
        User,
        user_id
    )
    if user is None:
        raise UserNotFoundException()
    return user