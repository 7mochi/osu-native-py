from __future__ import annotations

from ctypes import byref
from typing import Dict

from ...native import ManagedObjectHandle
from ...native import NativeRuleset
from ...native import bindings
from .error_code import ErrorCode
from .native_helper import NativeHelper


class Ruleset:
    _RULESET_SHORT_NAME_BY_ID: Dict[int, str] = {0: "osu", 1: "taiko", 2: "catch", 3: "mania"}

    def __init__(self, native_ruleset: NativeRuleset):
        self._native = native_ruleset
        self._closed = False

    @classmethod
    def from_id(cls, ruleset_id: int) -> Ruleset:
        native_ruleset = bindings.NativeRuleset()

        result = bindings.Ruleset_CreateFromId(ruleset_id, byref(native_ruleset))
        NativeHelper.check_error(result, f"create ruleset from ID {ruleset_id}")

        return cls(native_ruleset)

    @property
    def handle(self) -> ManagedObjectHandle:
        return self._native.handle

    @property
    def ruleset_id(self) -> int:
        self._check_not_closed()
        return self._native.rulesetId

    @property
    def short_name(self) -> str:
        self._check_not_closed()
        return self._RULESET_SHORT_NAME_BY_ID.get(self.ruleset_id, f"unknown({self.ruleset_id})")

    @property
    def is_closed(self) -> bool:
        return self._closed

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Ruleset has been closed")

    def close(self) -> None:
        if not self._closed:
            bindings.Ruleset_Destroy(self.handle)
            self._closed = True

    def __enter__(self) -> Ruleset:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        if self._closed:
            return f"<Ruleset (closed)>"
        return f"<Ruleset id={self.ruleset_id} name='{self.short_name}'>"

    def __str__(self) -> str:
        if self._closed:
            return "Ruleset{closed=true}"
        return f"Ruleset{{rulesetId={self.ruleset_id}, shortName='{self.short_name}'}}"
