from fastapi import APIRouter, Path, status, Depends, Query
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies.user import get_user_service
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import CurrentUser
from app.dependencies.authorization import AdminUser

router = APIRouter()

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    _: AdminUser,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.create_user(db, user)

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    _: AdminUser,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    skip = (page - 1) * size
    return service.get_users(
        db,
        skip=skip,
        limit=size
    )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_current_user(
    user: CurrentUser
):
    return user

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    _: AdminUser,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    user = service.get_user(db, user_id)
    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_data: UserUpdate,
    _: AdminUser,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    user = service.update_user(
        db,
        user_id,
        user_data
    )
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    _: AdminUser,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
):
    return service.delete_user(
        db,
        user_id
    )