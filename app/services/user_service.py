from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import UserNotFoundException, EmailAlreadyExistsException


class UserService:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    def create_user(
        self,
        db: Session,
        user_data: UserCreate
    ) -> User:

        existing_user = self.repository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise EmailAlreadyExistsException(user_data.email)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )

        return self.repository.create(db, user)

    def get_user(
        self,
        db: Session,
        user_id: int
    ) -> User | None:

        user = self.repository.get_by_id(
            db,
            user_id
        )
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def get_users(
        self,
        db: Session,
        skip: int,
        limit: int
    ) -> list[User]:

        return self.repository.get_all(
            db,
            skip,
            limit
        )

    def update_user(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ) -> User | None:

        user = self.repository.get_by_id(
            db,
            user_id
        )

        if not user:
            raise UserNotFoundException(user_id)

        if user_data.name is not None:
            user.name = user_data.name

        if user_data.email is not None:
            user.email = user_data.email

        db.commit()
        db.refresh(user)

        return user

    def delete_user(
        self,
        db: Session,
        user_id: int
    ) -> bool:

        user = self.repository.get_by_id(
            db,
            user_id
        )

        if not user:
            return UserNotFoundException(user_id)

        self.repository.delete(db, user)

        return True