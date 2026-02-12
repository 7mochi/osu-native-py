from __future__ import annotations

from ctypes import byref
from typing import Dict

from ...native import NativeRuleset
from ...native import bindings
from ..utils.native_handler import NativeHandler


class Ruleset(NativeHandler):
    """Represents an osu! ruleset.

    Required when creating difficulty calculators and calculating performance.
    Specifies which ruleset to use: osu!standard (0), osu!taiko (1), osu!catch (2),
    or osu!mania (3).
    """

    _RULESET_SHORT_NAME_BY_ID: Dict[int, str] = {0: "osu", 1: "taiko", 2: "catch", 3: "mania"}

    def __init__(self, native_ruleset: NativeRuleset):
        super().__init__(native_ruleset)

    @classmethod
    def from_id(cls, ruleset_id: int) -> Ruleset:
        """Create a ruleset from its numeric ID.

        Args:
            ruleset_id: The ruleset ID (0=osu, 1=taiko, 2=catch, 3=mania).

        Returns:
            A new Ruleset instance.

        Raises:
            RuntimeError: If the ruleset creation fails or the ID is invalid.
        """
        native_ruleset = bindings.NativeRuleset()

        result = bindings.Ruleset_CreateFromId(ruleset_id, byref(native_ruleset))
        cls.check_error(result, f"create ruleset from ID {ruleset_id}")

        return cls(native_ruleset)

    @property
    def ruleset_id(self) -> int:
        """The numeric ID of the ruleset.

        Returns:
            0 for osu!standard, 1 for taiko, 2 for catch, 3 for mania.

        Raises:
            RuntimeError: If the ruleset is already closed.
        """
        self._check_not_closed()
        return self._native.rulesetId

    @property
    def short_name(self) -> str:
        """The short name of the ruleset.

        Returns:
            "osu", "taiko", "catch", or "mania". Returns "unknown(id)" for invalid IDs.

        Raises:
            RuntimeError: If the ruleset is already closed.
        """
        self._check_not_closed()
        return self._RULESET_SHORT_NAME_BY_ID.get(self.ruleset_id, f"unknown({self.ruleset_id})")

    def _destroy(self) -> None:
        bindings.Ruleset_Destroy(self.handle)

    def __repr__(self) -> str:
        if self.is_closed:
            return f"<Ruleset (closed)>"

        return f"<Ruleset id={self.ruleset_id} name='{self.short_name}'>"

    def __str__(self) -> str:
        if self.is_closed:
            return "Ruleset{closed=true}"

        return f"Ruleset{{rulesetId={self.ruleset_id}, shortName='{self.short_name}'}}"
