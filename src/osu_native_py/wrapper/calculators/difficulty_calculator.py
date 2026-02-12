from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from ctypes import byref

from ...native import ManagedObjectHandle
from ...native import bindings
from ..attributes.difficulty import CatchDifficultyAttributes
from ..attributes.difficulty import DifficultyAttributes
from ..attributes.difficulty import ManiaDifficultyAttributes
from ..attributes.difficulty import OsuDifficultyAttributes
from ..attributes.difficulty import TaikoDifficultyAttributes
from ..objects import Beatmap
from ..objects import ModsCollection
from ..objects import Ruleset
from ..utils.native_handler import NativeHandler


class DifficultyCalculator(NativeHandler, ABC):
    def __init__(self, handle: ManagedObjectHandle):
        super().__init__(handle)

    @abstractmethod
    def calculate(self, mods: ModsCollection) -> DifficultyAttributes:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class OsuDifficultyCalculator(DifficultyCalculator):
    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> OsuDifficultyCalculator:
        native_calc = bindings.NativeOsuDifficultyCalculator()
        result = bindings.OsuDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create OsuDifficultyCalculator")
        return cls(native_calc.handle)

    def calculate(self, mods: ModsCollection) -> OsuDifficultyAttributes:
        self._check_not_closed()

        native_diff = bindings.NativeOsuDifficultyAttributes()
        result = bindings.OsuDifficultyCalculator_Calculate(
            self.handle,
            mods.handle,
            byref(native_diff),
        )
        self.check_error(result, "calculate osu! difficulty")

        return OsuDifficultyAttributes.from_native(native_diff)

    def close(self) -> None:
        if not self._closed:
            bindings.OsuDifficultyCalculator_Destroy(self.handle)
            self._closed = True


class TaikoDifficultyCalculator(DifficultyCalculator):
    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> TaikoDifficultyCalculator:
        native_calc = bindings.NativeTaikoDifficultyCalculator()
        result = bindings.TaikoDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create TaikoDifficultyCalculator")
        return cls(native_calc.handle)

    def calculate(self, mods: ModsCollection) -> TaikoDifficultyAttributes:
        self._check_not_closed()

        native_diff = bindings.NativeTaikoDifficultyAttributes()
        result = bindings.TaikoDifficultyCalculator_Calculate(
            self.handle,
            mods.handle,
            byref(native_diff),
        )
        self.check_error(result, "calculate Taiko difficulty")

        return TaikoDifficultyAttributes.from_native(native_diff)

    def close(self) -> None:
        if not self._closed:
            bindings.TaikoDifficultyCalculator_Destroy(self.handle)
            self._closed = True


class CatchDifficultyCalculator(DifficultyCalculator):
    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> CatchDifficultyCalculator:
        native_calc = bindings.NativeCatchDifficultyCalculator()
        result = bindings.CatchDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create CatchDifficultyCalculator")
        return cls(native_calc.handle)

    def calculate(self, mods: ModsCollection) -> CatchDifficultyAttributes:
        self._check_not_closed()

        native_diff = bindings.NativeCatchDifficultyAttributes()
        result = bindings.CatchDifficultyCalculator_Calculate(
            self.handle,
            mods.handle,
            byref(native_diff),
        )
        self.check_error(result, "calculate Catch difficulty")

        return CatchDifficultyAttributes.from_native(native_diff)

    def close(self) -> None:
        if not self._closed:
            bindings.CatchDifficultyCalculator_Destroy(self.handle)
            self._closed = True


class ManiaDifficultyCalculator(DifficultyCalculator):
    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> ManiaDifficultyCalculator:
        native_calc = bindings.NativeManiaDifficultyCalculator()
        result = bindings.ManiaDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create ManiaDifficultyCalculator")
        return cls(native_calc.handle)

    def calculate(self, mods: ModsCollection) -> ManiaDifficultyAttributes:
        self._check_not_closed()

        native_diff = bindings.NativeManiaDifficultyAttributes()
        result = bindings.ManiaDifficultyCalculator_Calculate(
            self.handle,
            mods.handle,
            byref(native_diff),
        )
        self.check_error(result, "calculate Mania difficulty")

        return ManiaDifficultyAttributes.from_native(native_diff)

    def close(self) -> None:
        if not self._closed:
            bindings.ManiaDifficultyCalculator_Destroy(self.handle)
            self._closed = True


def create_difficulty_calculator(ruleset: Ruleset, beatmap: Beatmap) -> DifficultyCalculator:
    ruleset_id = ruleset.ruleset_id

    if ruleset_id == 0:
        return OsuDifficultyCalculator.create(ruleset, beatmap)
    elif ruleset_id == 1:
        return TaikoDifficultyCalculator.create(ruleset, beatmap)
    elif ruleset_id == 2:
        return CatchDifficultyCalculator.create(ruleset, beatmap)
    elif ruleset_id == 3:
        return ManiaDifficultyCalculator.create(ruleset, beatmap)
    else:
        raise ValueError(f"Unsupported ruleset ID: {ruleset_id}")
