from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from ctypes import byref
from ctypes import c_int32
from typing import List
from typing import Union

from ...native import NativeCatchDifficultyCalculator
from ...native import NativeManiaDifficultyCalculator
from ...native import NativeOsuDifficultyCalculator
from ...native import NativeTaikoDifficultyCalculator
from ...native import bindings
from ..attributes.difficulty import CatchDifficultyAttributes
from ..attributes.difficulty import DifficultyAttributes
from ..attributes.difficulty import ManiaDifficultyAttributes
from ..attributes.difficulty import OsuDifficultyAttributes
from ..attributes.difficulty import TaikoDifficultyAttributes
from ..attributes.difficulty import TimedCatchDifficultyAttributes
from ..attributes.difficulty import TimedManiaDifficultyAttributes
from ..attributes.difficulty import TimedOsuDifficultyAttributes
from ..attributes.difficulty import TimedTaikoDifficultyAttributes
from ..objects import Beatmap
from ..objects import ModsCollection
from ..objects import Ruleset
from ..objects.error_code import ErrorCode
from ..utils.native_handler import NativeHandler


class DifficultyCalculator(NativeHandler, ABC):
    """Base class for difficulty calculators.

    Calculates the difficulty of a beatmap using a specific mod combination.
    This is an abstract base class that must be subclassed for each game mode.
    """

    def __init__(
        self,
        handle: Union[
            NativeOsuDifficultyCalculator,
            NativeTaikoDifficultyCalculator,
            NativeCatchDifficultyCalculator,
            NativeManiaDifficultyCalculator,
        ],
    ):
        super().__init__(handle)

    @abstractmethod
    def calculate(self, mods: ModsCollection) -> DifficultyAttributes:
        """Calculate the difficulty of the beatmap with the given mods.

        Args:
            mods: The mods to apply to the beatmap.

        Returns:
            A structure describing the difficulty of the beatmap.
        """

    @abstractmethod
    def calculate_timed(self, mods: ModsCollection) -> List[
        Union[
            TimedOsuDifficultyAttributes,
            TimedTaikoDifficultyAttributes,
            TimedCatchDifficultyAttributes,
            TimedManiaDifficultyAttributes,
        ]
    ]:
        """Calculate difficulty attributes at each hit object."""

    def _calculate_timed(self, mods, native_type, calculate, attributes_type):
        self._check_not_closed()
        size = c_int32()
        result = calculate(self.handle, mods.handle, None, byref(size))
        if result != ErrorCode.BUFFER_SIZE_QUERY:
            self.check_error(result, "query timed difficulty size")
            raise RuntimeError(f"Unexpected buffer query result: {result}")

        buffer = (native_type * size.value)()
        result = calculate(self.handle, mods.handle, buffer, byref(size))
        self.check_error(result, "calculate timed difficulty")
        return [attributes_type.from_native(value) for value in buffer[: size.value]]


class OsuDifficultyCalculator(DifficultyCalculator):
    """Difficulty calculator for osu!standard mode."""

    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> OsuDifficultyCalculator:
        native_calc = bindings.NativeOsuDifficultyCalculator()
        result = bindings.OsuDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create OsuDifficultyCalculator")
        return cls(native_calc)

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

    def calculate_timed(self, mods: ModsCollection) -> List[TimedOsuDifficultyAttributes]:
        return self._calculate_timed(
            mods,
            bindings.NativeTimedOsuDifficultyAttributes,
            bindings.OsuDifficultyCalculator_CalculateTimed,
            TimedOsuDifficultyAttributes,
        )

    def _destroy(self) -> None:
        bindings.OsuDifficultyCalculator_Destroy(self.handle)


class TaikoDifficultyCalculator(DifficultyCalculator):
    """Difficulty calculator for osu!taiko mode."""

    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> TaikoDifficultyCalculator:
        native_calc = bindings.NativeTaikoDifficultyCalculator()
        result = bindings.TaikoDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create TaikoDifficultyCalculator")
        return cls(native_calc)

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

    def calculate_timed(self, mods: ModsCollection) -> List[TimedTaikoDifficultyAttributes]:
        return self._calculate_timed(
            mods,
            bindings.NativeTimedTaikoDifficultyAttributes,
            bindings.TaikoDifficultyCalculator_CalculateTimed,
            TimedTaikoDifficultyAttributes,
        )

    def _destroy(self) -> None:
        bindings.TaikoDifficultyCalculator_Destroy(self.handle)


class CatchDifficultyCalculator(DifficultyCalculator):
    """Difficulty calculator for osu!catch mode."""

    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> CatchDifficultyCalculator:
        native_calc = bindings.NativeCatchDifficultyCalculator()
        result = bindings.CatchDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create CatchDifficultyCalculator")
        return cls(native_calc)

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

    def calculate_timed(self, mods: ModsCollection) -> List[TimedCatchDifficultyAttributes]:
        return self._calculate_timed(
            mods,
            bindings.NativeTimedCatchDifficultyAttributes,
            bindings.CatchDifficultyCalculator_CalculateTimed,
            TimedCatchDifficultyAttributes,
        )

    def _destroy(self) -> None:
        bindings.CatchDifficultyCalculator_Destroy(self.handle)


class ManiaDifficultyCalculator(DifficultyCalculator):
    """Difficulty calculator for osu!mania mode."""

    @classmethod
    def create(cls, ruleset: Ruleset, beatmap: Beatmap) -> ManiaDifficultyCalculator:
        native_calc = bindings.NativeManiaDifficultyCalculator()
        result = bindings.ManiaDifficultyCalculator_Create(
            ruleset.handle,
            beatmap.handle,
            byref(native_calc),
        )
        cls.check_error(result, "create ManiaDifficultyCalculator")
        return cls(native_calc)

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

    def calculate_timed(self, mods: ModsCollection) -> List[TimedManiaDifficultyAttributes]:
        return self._calculate_timed(
            mods,
            bindings.NativeTimedManiaDifficultyAttributes,
            bindings.ManiaDifficultyCalculator_CalculateTimed,
            TimedManiaDifficultyAttributes,
        )

    def _destroy(self) -> None:
        bindings.ManiaDifficultyCalculator_Destroy(self.handle)


def create_difficulty_calculator(ruleset: Ruleset, beatmap: Beatmap) -> DifficultyCalculator:
    """Create a difficulty calculator for the specified ruleset.

    Args:
        ruleset: The ruleset to create a calculator for.
        beatmap: The beatmap to calculate difficulty for.

    Returns:
        A difficulty calculator appropriate for the ruleset.

    Raises:
        ValueError: If the ruleset ID is not supported (must be 0-3).
    """
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
