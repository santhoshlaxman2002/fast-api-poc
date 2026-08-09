from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.exceptions import InvalidCredentialsException

class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, db, email: str, password: str):
        user = self.repository.get_by_email(db, email)
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        return user

    def create_token(self, user) -> str:
        return create_access_token({"sub": str(user.id)})