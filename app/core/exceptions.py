class AppException(Exception):
    def __init__(
        self, 
        message: str,
        status_code:int,
        code:str = "APP_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.code = code

        super().__init__(message)

class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        if user_id is None:
            message = "User not found"
        else:
            message = f"User with ID {user_id} not found"
        super().__init__(message, status_code=404, code="USER_NOT_FOUND")

class EmailAlreadyExistsException(AppException):
    def __init__(self, email: str):
        message = f"Email {email} already exists"
        super().__init__(message, status_code=409, code="EMAIL_ALREADY_EXISTS")

class InvalidCredentialsException(AppException):
    def __init__(self):
        message = "Invalid email or password"
        super().__init__(message, status_code=401, code="INVALID_CREDENTIALS")

class InvalidTokenException(AppException):
    def __init__(self):
        message = "Invalid token"
        super().__init__(message, status_code=401, code="INVALID_TOKEN")

class InvalidAuthenticationCredentialsException(AppException):
    def __init__(self):
        message = "Invalid authentication credentials"
        super().__init__(message, status_code=401, code="INVALID_AUTH_CREDENTIALS")

class InsufficientPermissionsException(AppException):
    def __init__(self):
        message = "Insufficient permissions"
        super().__init__(message, status_code=403, code="INSUFFICIENT_PERMISSIONS")

class UnsupportedFileTypeExecption(AppException):
    def __init__(self):
        message = "Unsupported file type"
        super().__init__(message, status_code=400, code="UNSUPPORTED_FILE_TYPE")

class FileTooLargeExecption(AppException):
    def __init__(self):
        message = "File too large"
        super().__init__(message, status_code=413, code="FILE_TOO_LARGE")