from __future__ import annotations

from ctypes import byref
from typing import List

from ...native import ManagedObjectHandle
from ...native import NativeModsCollection
from ...native import bindings
from .error_code import ErrorCode
from .mod import Mod
from .native_handler import NativeHandler


class ModsCollection(NativeHandler):
    def __init__(self, native_mods_collection: NativeModsCollection):
        super().__init__(native_mods_collection)
        self._mods: List[Mod] = []

    @classmethod
    def create(cls) -> ModsCollection:
        native_mods_collection = bindings.NativeModsCollection()

        result = bindings.ModsCollection_Create(byref(native_mods_collection))
        cls.check_error(result, "create mods collection")

        return cls(native_mods_collection)

    def add(self, mod: Mod) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Add(self.handle, mod.handle)
        self.check_error(result, "add mod to collection")
        self._mods.append(mod)

    def has(self, mod: Mod) -> bool:
        return mod in self._mods

    def remove(self, mod: Mod) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Remove(self.handle, mod.handle)
        self.check_error(result, "remove mod from collection")
        if mod in self._mods:
            self._mods.remove(mod)

    def debug(self) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Debug(self.handle)
        if result != ErrorCode.SUCCESS:
            print(f"Debug failed: {ErrorCode.from_value(result)}")

    def _destroy(self) -> None:
        for mod in self._mods:
            try:
                if not mod.is_closed:
                    mod.close()
            except Exception:
                pass

        bindings.ModsCollection_Destroy(self.handle)

    def __repr__(self) -> str:
        if self.is_closed:
            return f"<ModsCollection (closed)>"

        return f"<ModsCollection handle={self.handle.id} mods={len(self._mods)}>"
