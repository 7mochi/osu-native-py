from __future__ import annotations

from ctypes import byref
from typing import List

from ...native import ManagedObjectHandle
from ...native import NativeModsCollection
from ...native import bindings
from .error_code import ErrorCode
from .mod import Mod
from .native_helper import NativeHelper


class ModsCollection:
    def __init__(self, native_mods_collection: NativeModsCollection):
        self._native = native_mods_collection
        self._mods: List[Mod] = []
        self._closed = False

    @classmethod
    def create(cls) -> ModsCollection:
        native_mods_collection = bindings.NativeModsCollection()

        result = bindings.ModsCollection_Create(byref(native_mods_collection))
        NativeHelper.check_error(result, "create mods collection")

        return cls(native_mods_collection)

    @property
    def handle(self) -> ManagedObjectHandle:
        return self._native.handle

    def add(self, mod: Mod) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Add(self.handle, mod.handle)
        NativeHelper.check_error(result, "add mod to collection")
        self._mods.append(mod)

    def has(self, mod: Mod) -> bool:
        return mod in self._mods

    def remove(self, mod: Mod) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Remove(self.handle, mod.handle)
        NativeHelper.check_error(result, "remove mod from collection")
        if mod in self._mods:
            self._mods.remove(mod)

    def debug(self) -> None:
        self._check_not_closed()
        result = bindings.ModsCollection_Debug(self.handle)
        if result != ErrorCode.SUCCESS:
            print(f"Debug failed: {ErrorCode.from_value(result)}")

    @property
    def is_closed(self) -> bool:
        return self._closed

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError("ModsCollection has been closed")

    def close(self) -> None:
        if not self._closed:
            for mod in self._mods:
                try:
                    if not mod.is_closed:
                        mod.close()
                except Exception:
                    pass

            bindings.ModsCollection_Destroy(self.handle)
            self._closed = True

    def __enter__(self) -> ModsCollection:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        if self._closed:
            return f"<ModsCollection (closed)>"
        return f"<ModsCollection handle={self.handle.id} mods={len(self._mods)}>"
