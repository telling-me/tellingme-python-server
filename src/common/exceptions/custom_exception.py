from typing import Any

from common.exceptions.error_code import ErrorCode


class CustomException(Exception):
    def __init__(self, error_code: ErrorCode) -> None:
        self.error_code = error_code
        super().__init__(error_code.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.error_code.code,
            "message": self.error_code.message,
            "data": None,
        }
