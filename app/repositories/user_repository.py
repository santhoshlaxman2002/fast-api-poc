from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def create(
        self,
        db: Session,
        user: User
    ) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_by_id(
        self,
        db: Session,
        user_id: int
    ) -> User | None:
        return db.get(User, user_id)

    def get_by_email(
        self,
        db: Session,
        email: str
    ) -> User | None:
        statement = select(User).where(User.email == email)
        return db.scalar(statement)

    def get_all(
        self,
        db: Session,
        skip:int = 0,
        limit:int = 10
    ) -> list[User]:
        statement = (
            select(User)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    def delete(
        self,
        db: Session,
        user: User
    ) -> None:
        db.delete(user)
        db.commit()