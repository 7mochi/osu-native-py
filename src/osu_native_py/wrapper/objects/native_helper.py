"""
Utilidades helper para trabajar con funciones nativas.
"""

from __future__ import annotations

from ctypes import POINTER
from ctypes import byref
from ctypes import c_int32
from ctypes import c_uint8
from ctypes import create_string_buffer
from typing import Callable
from typing import Optional

from ...native import ManagedObjectHandle
from ...native import bindings
from .error_code import ErrorCode


class NativeHelper:
    @staticmethod
    def get_string(handle: ManagedObjectHandle, getter_func: Callable, max_size: int = 1024) -> str:
        buffer_size = c_int32(0)
        result = getter_func(handle, None, byref(buffer_size))

        if result != ErrorCode.BUFFER_SIZE_QUERY:
            raise RuntimeError(
                f"Error querying buffer size: {ErrorCode.from_value(result)}",
            )

        if buffer_size.value <= 0:
            return ""

        buffer = (c_uint8 * buffer_size.value)()
        result = getter_func(handle, buffer, byref(buffer_size))

        if result != ErrorCode.SUCCESS:
            raise RuntimeError(f"Error getting string: {ErrorCode.from_value(result)}")

        return bytes(buffer[: buffer_size.value]).decode("utf-8").rstrip("\x00")

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
