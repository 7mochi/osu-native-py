from __future__ import annotations

from enum import IntEnum


class ErrorCode(IntEnum):
    """Error codes returned from native operations.

    Values:
        < 0: Special codes (not errors)
        0: Success
        > 0: Error codes
    """

    END_OF_ENUMERATION = -2
    """Indicates that the end of an enumeration was reached."""

    BUFFER_SIZE_QUERY = -1
    """Indicates that the required size of a buffer was queried."""

    SUCCESS = 0
    """Indicates a successful operation."""

    OBJECT_NOT_RESOLVED = 1
    """Indicates that the object referenced by a managed object handle was not resolved."""

    RULESET_UNAVAILABLE = 2
    """Indicates that the ruleset requested is not available (e.g., not found)."""

    UNEXPECTED_RULESET = 3
    """Indicates that the specified ruleset instance is not of the expected ruleset
    for the operation context (e.g., Osu ruleset instance passed to a Catch
    difficulty calculator)."""

    FAILURE = 127
    """Indicates an unspecific operation failure."""

    @classmethod
    def from_value(cls, value: int) -> ErrorCode:
        """Convert an integer value to an ErrorCode.

        Args:
            value: The integer value to convert.

        Returns:
            The corresponding ErrorCode, or FAILURE if the value is not recognized.
        """
        try:
            return cls(value)
        except ValueError:
            return cls.FAILURE

    def is_success(self) -> bool:
        """Check if this error code represents success.

        Returns:
            True if this is SUCCESS, False otherwise.
        """
        return self == ErrorCode.SUCCESS

    def __str__(self) -> str:
        return self.name
