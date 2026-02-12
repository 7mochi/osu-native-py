from __future__ import annotations

from ctypes import byref

from ...native import NativeMod
from ...native import bindings
from ..utils.native_handler import NativeHandler


class Mod(NativeHandler):
    def __init__(self, native_mod: NativeMod):
        super().__init__(native_mod)

    @classmethod
    def create(cls, acronym: str) -> Mod:
        native_string = cls.create_native_string(acronym)
        native_mod = bindings.NativeMod()

        result = bindings.Mod_Create(native_string, byref(native_mod))
        cls.check_error(result, f"create mod '{acronym}'")

        return cls(native_mod)

    def set_setting_bool(self, key: str, value: bool) -> None:
        self._check_not_closed()
        native_key = self.create_native_string(key)
        result = bindings.Mod_SetSettingBool(self.handle, native_key, value)
        self.check_error(result, f"set mod setting '{key}' to {value}")

    def set_setting_int(self, key: str, value: int) -> None:
        self._check_not_closed()
        native_key = self.create_native_string(key)
        result = bindings.Mod_SetSettingInteger(self.handle, native_key, value)
        self.check_error(result, f"set mod setting '{key}' to {value}")

    def set_setting_float(self, key: str, value: float) -> None:
        self._check_not_closed()
        native_key = self.create_native_string(key)
        result = bindings.Mod_SetSettingFloat(self.handle, native_key, value)
        self.check_error(result, f"set mod setting '{key}' to {value}")

    def _destroy(self) -> None:
        bindings.Mod_Destroy(self.handle)

    def __repr__(self) -> str:
        if self.is_closed:
            return f"<Mod (closed)>"
        return f"<Mod handle={self.handle.id}>"
