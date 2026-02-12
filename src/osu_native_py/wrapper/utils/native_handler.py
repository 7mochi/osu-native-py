from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from ctypes import byref
from ctypes import c_int32
from ctypes import c_uint8
from typing import Any
from typing import Callable

from ...native import ManagedObjectHandle
from ..objects.error_code import ErrorCode


class NativeHandler(ABC):
    def __init__(self, native: Any):
        self._native = native
        self._closed = False

    @property
    def handle(self) -> ManagedObjectHandle:
        return self._native.handle

    @property
    def is_closed(self) -> bool:
        return self._closed

    @staticmethod
    def create_native_string(text: str):
        encoded = text.encode("utf-8")
        buffer = (c_uint8 * (len(encoded) + 1))()
        for i, byte in enumerate(encoded):
            buffer[i] = byte
        buffer[len(encoded)] = 0
        return buffer

    @staticmethod
    def check_error(result: int, operation: str) -> None:
        error_code = ErrorCode.from_value(result)
        if not error_code.is_success():
            raise RuntimeError(f"Failed to {operation}. Error: {error_code}")

    def get_string(self, getter_func: Callable, max_size: int = 1024) -> str:
        buffer_size = c_int32(0)
        result = getter_func(self.handle, None, byref(buffer_size))

        if result != ErrorCode.BUFFER_SIZE_QUERY:
            raise RuntimeError(f"Error querying buffer size: {ErrorCode.from_value(result)}")

        if buffer_size.value <= 0:
            return ""

        buffer = (c_uint8 * buffer_size.value)()
        result = getter_func(self.handle, buffer, byref(buffer_size))

        if result != ErrorCode.SUCCESS:
            raise RuntimeError(f"Error getting string: {ErrorCode.from_value(result)}")

        return bytes(buffer[: buffer_size.value]).decode("utf-8").rstrip("\x00")

    def close(self) -> None:
        if self._closed:
            return

        self._destroy()
        self._closed = True

    @abstractmethod
    def _destroy(self) -> None:
        raise NotImplementedError()

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError(f"{self.__class__.__name__} has been closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def __repr__(self) -> str:
        if self._closed:
            return f"<{self.__class__.__name__} (closed)>"
        try:
            return f"<{self.__class__.__name__} handle={self.handle.id}>"
        except Exception:
            return f"<{self.__class__.__name__}>"
