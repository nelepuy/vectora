# -*- coding: utf-8 -*-
"""
Централизованные исключения приложения.
"""
from fastapi import HTTPException, status


class VectoraException(HTTPException):
    """Базовый класс для всех исключений приложения."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class TaskNotFoundError(VectoraException):
    """Задача не найдена."""
    def __init__(self, task_id: int):
        super().__init__(
            detail=f"Задача с ID {task_id} не найдена",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationError(VectoraException):
    """Ошибка валидации данных."""
    def __init__(self, message: str):
        super().__init__(
            detail=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class UnauthorizedError(VectoraException):
    """Ошибка аутентификации."""
    def __init__(self, message: str = "Необходима авторизация"):
        super().__init__(
            detail=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ForbiddenError(VectoraException):
    """Недостаточно прав."""
    def __init__(self, message: str = "Недостаточно прав для выполнения операции"):
        super().__init__(
            detail=message,
            status_code=status.HTTP_403_FORBIDDEN
        )


class DatabaseError(VectoraException):
    """Ошибка базы данных."""
    def __init__(self, message: str = "Ошибка при работе с базой данных"):
        super().__init__(
            detail=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
