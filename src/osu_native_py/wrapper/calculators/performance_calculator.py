from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from ctypes import byref
from typing import Union

from ...native import NativeCatchPerformanceCalculator
from ...native import NativeManiaPerformanceCalculator
from ...native import NativeOsuPerformanceCalculator
from ...native import NativeTaikoPerformanceCalculator
from ...native import bindings
from ..attributes.difficulty import CatchDifficultyAttributes
from ..attributes.difficulty import DifficultyAttributes
from ..attributes.difficulty import ManiaDifficultyAttributes
from ..attributes.difficulty import OsuDifficultyAttributes
from ..attributes.difficulty import TaikoDifficultyAttributes
from ..attributes.performance import CatchPerformanceAttributes
from ..attributes.performance import ManiaPerformanceAttributes
from ..attributes.performance import OsuPerformanceAttributes
from ..attributes.performance import PerformanceAttributes
from ..attributes.performance import TaikoPerformanceAttributes
from ..objects import Beatmap
from ..objects import ModsCollection
from ..objects import Ruleset
from ..objects import ScoreInfo
from ..utils.native_handler import NativeHandler


class PerformanceCalculator(NativeHandler, ABC):
    """Base class for performance calculators.

    Calculates the performance attributes of a score on a beatmap.
    This is an abstract base class that must be subclassed for each game mode.
    """

    def __init__(
        self,
        handle: Union[
            NativeOsuPerformanceCalculator,
            NativeTaikoPerformanceCalculator,
            NativeCatchPerformanceCalculator,
            NativeManiaPerformanceCalculator,
        ],
    ):
        super().__init__(handle)

    @abstractmethod
    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> PerformanceAttributes:
        """Calculate the performance attributes of a score.

        Args:
            ruleset: The ruleset for the beatmap.
            beatmap: The beatmap the score was set on.
            mods: The mods to apply to the beatmap.
            score_info: Information about the score.
            difficulty_attributes: The difficulty attributes for the beatmap.

        Returns:
            A structure describing the performance of the score.
        """


class OsuPerformanceCalculator(PerformanceCalculator):
    """Performance calculator for osu!standard mode."""

    @classmethod
    def create(cls) -> OsuPerformanceCalculator:
        native_calc = bindings.NativeOsuPerformanceCalculator()
        result = bindings.OsuPerformanceCalculator_Create(byref(native_calc))
        cls.check_error(result, "create OsuPerformanceCalculator")
        return cls(native_calc)

    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> OsuPerformanceAttributes:
        self._check_not_closed()

        if not isinstance(difficulty_attributes, OsuDifficultyAttributes):
            raise TypeError(
                f"Expected OsuDifficultyAttributes, got {type(difficulty_attributes).__name__}",
            )

        native_score = score_info.to_native(ruleset.handle, beatmap.handle, mods.handle)

        native_diff = difficulty_attributes.to_native()

        native_perf = bindings.NativeOsuPerformanceAttributes()
        result = bindings.OsuPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        self.check_error(result, "calculate osu! performance")

        return OsuPerformanceAttributes.from_native(native_perf)

    def _destroy(self) -> None:
        bindings.OsuPerformanceCalculator_Destroy(self.handle)


class TaikoPerformanceCalculator(PerformanceCalculator):
    """Performance calculator for osu!taiko mode."""

    @classmethod
    def create(cls) -> TaikoPerformanceCalculator:
        native_calc = bindings.NativeTaikoPerformanceCalculator()
        result = bindings.TaikoPerformanceCalculator_Create(byref(native_calc))
        cls.check_error(result, "create TaikoPerformanceCalculator")
        return cls(native_calc)

    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> TaikoPerformanceAttributes:
        self._check_not_closed()

        if not isinstance(difficulty_attributes, TaikoDifficultyAttributes):
            raise TypeError(
                f"Expected TaikoDifficultyAttributes, got {type(difficulty_attributes).__name__}",
            )

        native_score = score_info.to_native(ruleset.handle, beatmap.handle, mods.handle)

        native_diff = difficulty_attributes.to_native()

        native_perf = bindings.NativeTaikoPerformanceAttributes()
        result = bindings.TaikoPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        self.check_error(result, "calculate Taiko performance")

        return TaikoPerformanceAttributes.from_native(native_perf)

    def _destroy(self) -> None:
        bindings.TaikoPerformanceCalculator_Destroy(self.handle)


class CatchPerformanceCalculator(PerformanceCalculator):
    """Performance calculator for osu!catch mode."""

    @classmethod
    def create(cls) -> CatchPerformanceCalculator:
        native_calc = bindings.NativeCatchPerformanceCalculator()
        result = bindings.CatchPerformanceCalculator_Create(byref(native_calc))
        cls.check_error(result, "create CatchPerformanceCalculator")
        return cls(native_calc)

    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> CatchPerformanceAttributes:
        self._check_not_closed()

        if not isinstance(difficulty_attributes, CatchDifficultyAttributes):
            raise TypeError(
                f"Expected CatchDifficultyAttributes, got {type(difficulty_attributes).__name__}",
            )

        native_score = score_info.to_native(ruleset.handle, beatmap.handle, mods.handle)

        native_diff = difficulty_attributes.to_native()

        native_perf = bindings.NativeCatchPerformanceAttributes()
        result = bindings.CatchPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        self.check_error(result, "calculate Catch performance")

        return CatchPerformanceAttributes.from_native(native_perf)

    def _destroy(self) -> None:
        bindings.CatchPerformanceCalculator_Destroy(self.handle)


class ManiaPerformanceCalculator(PerformanceCalculator):
    """Performance calculator for osu!mania mode."""

    @classmethod
    def create(cls) -> ManiaPerformanceCalculator:
        native_calc = bindings.NativeManiaPerformanceCalculator()
        result = bindings.ManiaPerformanceCalculator_Create(byref(native_calc))
        cls.check_error(result, "create ManiaPerformanceCalculator")
        return cls(native_calc)

    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> ManiaPerformanceAttributes:
        self._check_not_closed()

        if not isinstance(difficulty_attributes, ManiaDifficultyAttributes):
            raise TypeError(
                f"Expected ManiaDifficultyAttributes, got {type(difficulty_attributes).__name__}",
            )

        native_score = score_info.to_native(ruleset.handle, beatmap.handle, mods.handle)

        native_diff = difficulty_attributes.to_native()

        native_perf = bindings.NativeManiaPerformanceAttributes()
        result = bindings.ManiaPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        self.check_error(result, "calculate Mania performance")

        return ManiaPerformanceAttributes.from_native(native_perf)

    def _destroy(self) -> None:
        bindings.ManiaPerformanceCalculator_Destroy(self.handle)


def create_performance_calculator(ruleset: Ruleset) -> PerformanceCalculator:
    """Create a performance calculator for the specified ruleset.

    Args:
        ruleset: The ruleset to create a calculator for.

    Returns:
        A performance calculator appropriate for the ruleset.

    Raises:
        ValueError: If the ruleset ID is not supported (must be 0-3).
    """
    ruleset_id = ruleset.ruleset_id

    if ruleset_id == 0:
        return OsuPerformanceCalculator.create()
    elif ruleset_id == 1:
        return TaikoPerformanceCalculator.create()
    elif ruleset_id == 2:
        return CatchPerformanceCalculator.create()
    elif ruleset_id == 3:
        return ManiaPerformanceCalculator.create()
    else:
        raise ValueError(f"Unsupported ruleset ID: {ruleset_id}")
