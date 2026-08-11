from typing import Callable, Annotated
from app.dependencies.auth import get_current_user
from app.models.user import User
from fastapi import Depends
from app.models.enum import UserRole
from app.core.exceptions import InsufficientPermissionsException

def require_role(
    *allowed_roles: UserRole
) -> Callable:
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsException  ()
        return current_user
    return role_checker

AdminUser = Annotated[
    User,
    Depends(require_role(UserRole.ADMIN))
]