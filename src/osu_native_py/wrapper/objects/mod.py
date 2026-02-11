from __future__ import annotations

from ctypes import byref

from ...native import ManagedObjectHandle
from ...native import NativeMod
from ...native import bindings
from .error_code import ErrorCode
from .native_helper import NativeHelper


class Mod:
    def __init__(self, native_mod: NativeMod):
        self._native = native_mod
        self._closed = False

    @classmethod
    def create(cls, acronym: str) -> Mod:
        native_string = NativeHelper.create_native_string(acronym)
        native_mod = bindings.NativeMod()

        result = bindings.Mod_Create(native_string, byref(native_mod))
        NativeHelper.check_error(result, f"create mod '{acronym}'")

        return cls(native_mod)

    @property
    def handle(self) -> ManagedObjectHandle:
        return self._native.handle

    def set_setting_bool(self, key: str, value: bool) -> None:
        self._check_not_closed()
        native_key = NativeHelper.create_native_string(key)
        result = bindings.Mod_SetSettingBool(self.handle, native_key, value)
        NativeHelper.check_error(result, f"set mod setting '{key}' to {value}")

    def set_setting_int(self, key: str, value: int) -> None:
        self._check_not_closed()
        native_key = NativeHelper.create_native_string(key)
        result = bindings.Mod_SetSettingInteger(self.handle, native_key, value)
        NativeHelper.check_error(result, f"set mod setting '{key}' to {value}")

    def set_setting_float(self, key: str, value: float) -> None:
        self._check_not_closed()
        native_key = NativeHelper.create_native_string(key)
        result = bindings.Mod_SetSettingFloat(self.handle, native_key, value)
        NativeHelper.check_error(result, f"set mod setting '{key}' to {value}")

    @property
    def is_closed(self) -> bool:
        return self._closed

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Mod has been closed")

    def close(self) -> None:
        if not self._closed:
            bindings.Mod_Destroy(self.handle)
            self._closed = True

    def __enter__(self) -> Mod:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        if self._closed:
            return f"<Mod (closed)>"
        return f"<Mod handle={self.handle.id}>"
