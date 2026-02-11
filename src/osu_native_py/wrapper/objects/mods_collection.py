"""
Wrapper para ModsCollection de osu-native.
"""

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
    """
    Representa una colección de mods de osu!.

    Esta clase mantiene referencias a los mods agregados para prevenir
    que sean garbage collected prematuramente.

    Ejemplo:
        with ModsCollection.create() as mods:
            dt = Mod.create("DT")
            mods.add(dt)
            hd = Mod.create("HD")
            mods.add(hd)
            # Usar mods en cálculos...
            # Los mods se cerrarán automáticamente al cerrar la colección
    """

    def __init__(self, native_mods_collection: NativeModsCollection):
        """
        Inicializa la ModsCollection con un NativeModsCollection existente.

        Args:
            native_mods_collection: El objeto NativeModsCollection de los bindings
        """
        self._native = native_mods_collection
        self._mods: List[Mod] = []  # Mantener referencias a los mods
        self._closed = False

    @classmethod
    def create(cls) -> ModsCollection:
        """
        Crea una nueva ModsCollection vacía.

        Returns:
            Una nueva instancia de ModsCollection

        Raises:
            RuntimeError: Si falla la creación
        """
        native_mods_collection = bindings.NativeModsCollection()

        result = bindings.ModsCollection_Create(byref(native_mods_collection))
        NativeHelper.check_error(result, "create mods collection")

        return cls(native_mods_collection)

    @property
    def handle(self) -> ManagedObjectHandle:
        """Retorna el handle del objeto nativo."""
        return self._native.handle

    def add(self, mod: Mod) -> None:
        """
        Agrega un mod a la colección.

        Args:
            mod: El mod a agregar

        Raises:
            RuntimeError: Si falla al agregar el mod
        """
        self._check_not_closed()
        result = bindings.ModsCollection_Add(self.handle, mod.handle)
        NativeHelper.check_error(result, "add mod to collection")
        # Mantener referencia para prevenir garbage collection
        self._mods.append(mod)

    def has(self, mod: Mod) -> bool:
        """
        Verifica si un mod está en la colección.

        Args:
            mod: El mod a verificar

        Returns:
            True si el mod está en la colección
        """
        return mod in self._mods

    def remove(self, mod: Mod) -> None:
        """
        Remueve un mod de la colección.

        Args:
            mod: El mod a remover

        Raises:
            RuntimeError: Si falla al remover el mod
        """
        self._check_not_closed()
        result = bindings.ModsCollection_Remove(self.handle, mod.handle)
        NativeHelper.check_error(result, "remove mod from collection")
        # Remover la referencia
        if mod in self._mods:
            self._mods.remove(mod)

    def debug(self) -> None:
        """
        Ejecuta la función de debug nativa para la colección.

        Útil para debugging y verificar el estado de la colección.
        """
        self._check_not_closed()
        result = bindings.ModsCollection_Debug(self.handle)
        if result != ErrorCode.SUCCESS:
            print(f"Debug failed: {ErrorCode.from_value(result)}")

    @property
    def is_closed(self) -> bool:
        """Retorna True si la colección ha sido cerrada."""
        return self._closed

    def _check_not_closed(self) -> None:
        """Verifica que la colección no haya sido cerrada."""
        if self._closed:
            raise RuntimeError("ModsCollection has been closed")

    def close(self) -> None:
        """
        Libera los recursos de la colección y cierra todos los mods.

        Primero cierra todos los mods individuales, luego destruye la colección.
        """
        if not self._closed:
            # Cerrar todos los mods primero
            for mod in self._mods:
                try:
                    if not mod.is_closed:
                        mod.close()
                except Exception:
                    # Ignorar errores al cerrar mods individuales
                    pass

            # Destruir la colección
            bindings.ModsCollection_Destroy(self.handle)
            self._closed = True

    def __enter__(self) -> ModsCollection:
        """Soporte para context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Limpieza automática al salir del context manager."""
        self.close()

    def __del__(self) -> None:
        """Destructor para asegurar que se liberen los recursos."""
        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        """Representación en string de la colección."""
        if self._closed:
            return f"<ModsCollection (closed)>"
        return f"<ModsCollection handle={self.handle.id} mods={len(self._mods)}>"
