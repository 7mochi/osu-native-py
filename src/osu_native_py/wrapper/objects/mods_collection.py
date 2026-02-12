from __future__ import annotations

from ctypes import byref
from typing import List

from ...native import NativeModsCollection
from ...native import bindings
from ..utils.native_handler import NativeHandler
from .error_code import ErrorCode
from .mod import Mod


class ModsCollection(NativeHandler):
    """Represents a collection of gameplay modifiers.

    Used when calculating difficulty or performance with multiple mods applied
    simultaneously (e.g., HD+DT+HR).
    """

    def __init__(self, native_mods_collection: NativeModsCollection):
        super().__init__(native_mods_collection)
        self._mods: List[Mod] = []

    @classmethod
    def create(cls) -> ModsCollection:
        """Create a new empty mods collection.

        Returns:
            A new empty collection.

        Raises:
            RuntimeError: If the collection creation fails.
        """
        native_mods_collection = bindings.NativeModsCollection()

        result = bindings.ModsCollection_Create(byref(native_mods_collection))
        cls.check_error(result, "create mods collection")

        return cls(native_mods_collection)

    def add(self, mod: Mod) -> None:
        """Adds a mod to the collection.

        Args:
            mod: The Mod instance to add to the collection.

        Raises:
            RuntimeError: If the collection is already closed or adding the mod fails.
        """
        self._check_not_closed()
        result = bindings.ModsCollection_Add(self.handle, mod.handle)
        self.check_error(result, "add mod to collection")
        self._mods.append(mod)

    def has(self, mod: Mod) -> bool:
        """Checks if a mod exists in the collection.

        Args:
            mod: The Mod instance to check for.

        Returns:
            bool: True if the mod is in the collection, False otherwise.
        """
        return mod in self._mods

    def remove(self, mod: Mod) -> None:
        """Removes a mod from the collection.

        Args:
            mod: The Mod instance to remove from the collection.

        Raises:
            RuntimeError: If the collection is already closed or removing the mod fails.
        """
        self._check_not_closed()
        result = bindings.ModsCollection_Remove(self.handle, mod.handle)
        self.check_error(result, "remove mod from collection")
        if mod in self._mods:
            self._mods.remove(mod)

    def debug(self) -> None:
        """Prints debug information about the collection to stdout.

        This is useful for debugging purposes to see the current state of the
        collection and all mods it contains.

        Raises:
            RuntimeError: If the collection is already closed.
        """
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
