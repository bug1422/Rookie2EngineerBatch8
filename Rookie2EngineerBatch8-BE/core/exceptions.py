from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotImplementedException(CustomException):
    def __init__(self, detail: str = "Not implemented"):
        super().__init__(status_code=501, detail=detail)

class DatabaseException(CustomException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)


class AuthenticationException(CustomException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=401, detail=detail)

class PasswordValidationException(CustomException):
    def __init__(self, detail: str = "Password is incorrect"):
        super().__init__(status_code=400, detail=detail)


class PermissionDeniedException(CustomException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=403, detail=detail)


class NotFoundException(CustomException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ValidationException(CustomException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)

class BusinessException(CustomException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
