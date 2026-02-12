from __future__ import annotations

from ctypes import byref
from typing import Dict

from ...native import ManagedObjectHandle
from ...native import NativeRuleset
from ...native import bindings
from .native_handler import NativeHandler


class Ruleset(NativeHandler):
    _RULESET_SHORT_NAME_BY_ID: Dict[int, str] = {0: "osu", 1: "taiko", 2: "catch", 3: "mania"}

    def __init__(self, native_ruleset: NativeRuleset):
        super().__init__(native_ruleset)

    @classmethod
    def from_id(cls, ruleset_id: int) -> Ruleset:
        native_ruleset = bindings.NativeRuleset()

        result = bindings.Ruleset_CreateFromId(ruleset_id, byref(native_ruleset))
        cls.check_error(result, f"create ruleset from ID {ruleset_id}")

        return cls(native_ruleset)

    @property
    def ruleset_id(self) -> int:
        self._check_not_closed()
        return self._native.rulesetId

    @property
    def short_name(self) -> str:
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
