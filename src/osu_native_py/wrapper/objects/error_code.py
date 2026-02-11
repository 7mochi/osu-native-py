from __future__ import annotations

from enum import IntEnum


class ErrorCode(IntEnum):
    END_OF_ENUMERATION = -2
    BUFFER_SIZE_QUERY = -1
    SUCCESS = 0
    OBJECT_NOT_RESOLVED = 1
    RULESET_UNAVAILABLE = 2
    UNEXPECTED_RULESET = 3
    FAILURE = 127

    @classmethod
    def from_value(cls, value: int) -> ErrorCode:
        try:
            return cls(value)
        except ValueError:
            return cls.FAILURE

    def is_success(self) -> bool:
        return self == ErrorCode.SUCCESS

    def __str__(self) -> str:
        return self.name
