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
from ..attributes.performance import CatchPerformanceAttributes
from ..attributes.performance import ManiaPerformanceAttributes
from ..attributes.performance import OsuPerformanceAttributes
from ..attributes.performance import PerformanceAttributes
from ..attributes.performance import TaikoPerformanceAttributes
from ..objects import Beatmap
from ..objects import ErrorCode
from ..objects import ModsCollection
from ..objects import NativeHelper
from ..objects import Ruleset
from ..objects import ScoreInfo


class PerformanceCalculator(ABC):
    def __init__(self, handle: ManagedObjectHandle):
        self._handle = handle
        self._closed = False

    @property
    def handle(self):
        return self._handle

    @property
    def is_closed(self) -> bool:
        return self._closed

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError(f"{self.__class__.__name__} has been closed")

    @abstractmethod
    def calculate(
        self,
        ruleset: Ruleset,
        beatmap: Beatmap,
        mods: ModsCollection,
        score_info: ScoreInfo,
        difficulty_attributes: DifficultyAttributes,
    ) -> PerformanceAttributes:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            self.close()


class OsuPerformanceCalculator(PerformanceCalculator):
    @classmethod
    def create(cls) -> OsuPerformanceCalculator:
        native_calc = bindings.NativeOsuPerformanceCalculator()
        result = bindings.OsuPerformanceCalculator_Create(byref(native_calc))
        NativeHelper.check_error(result, "create OsuPerformanceCalculator")
        return cls(native_calc.handle)

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

        native_diff = bindings.NativeOsuDifficultyAttributes()
        native_diff.starRating = difficulty_attributes.star_rating
        native_diff.maxCombo = difficulty_attributes.max_combo
        native_diff.aimDifficulty = difficulty_attributes.aim_difficulty
        native_diff.aimDifficultSliderCount = difficulty_attributes.aim_difficult_slider_count
        native_diff.speedDifficulty = difficulty_attributes.speed_difficulty
        native_diff.speedNoteCount = difficulty_attributes.speed_note_count
        native_diff.flashlightDifficulty = difficulty_attributes.flashlight_difficulty
        native_diff.sliderFactor = difficulty_attributes.slider_factor
        native_diff.aimTopWeightedSliderFactor = (
            difficulty_attributes.aim_top_weighted_slider_factor
        )
        native_diff.speedTopWeightedSliderFactor = (
            difficulty_attributes.speed_top_weighted_slider_factor
        )
        native_diff.aimDifficultStrainCount = difficulty_attributes.aim_difficult_strain_count
        native_diff.speedDifficultStrainCount = difficulty_attributes.speed_difficult_strain_count
        native_diff.nestedScorePerObject = difficulty_attributes.nested_score_per_object
        native_diff.legacyScoreBaseMultiplier = difficulty_attributes.legacy_score_base_multiplier
        native_diff.maximumLegacyComboScore = difficulty_attributes.maximum_legacy_combo_score
        native_diff.drainRate = difficulty_attributes.drain_rate
        native_diff.hitCircleCount = difficulty_attributes.hit_circle_count
        native_diff.sliderCount = difficulty_attributes.slider_count
        native_diff.spinnerCount = difficulty_attributes.spinner_count

        native_perf = bindings.NativeOsuPerformanceAttributes()
        result = bindings.OsuPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        NativeHelper.check_error(result, "calculate osu! performance")

        return OsuPerformanceAttributes.from_native(native_perf)

    def close(self) -> None:
        if not self._closed:
            bindings.OsuPerformanceCalculator_Destroy(self.handle)
            self._closed = True


class TaikoPerformanceCalculator(PerformanceCalculator):
    @classmethod
    def create(cls) -> TaikoPerformanceCalculator:
        native_calc = bindings.NativeTaikoPerformanceCalculator()
        result = bindings.TaikoPerformanceCalculator_Create(byref(native_calc))
        NativeHelper.check_error(result, "create TaikoPerformanceCalculator")
        return cls(native_calc.handle)

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

        native_diff = bindings.NativeTaikoDifficultyAttributes()
        native_diff.starRating = difficulty_attributes.star_rating
        native_diff.maxCombo = difficulty_attributes.max_combo
        native_diff.mechanicalDifficulty = difficulty_attributes.mechanical_difficulty
        native_diff.rhythmDifficulty = difficulty_attributes.rhythm_difficulty
        native_diff.readingDifficulty = difficulty_attributes.reading_difficulty
        native_diff.colourDifficulty = difficulty_attributes.colour_difficulty
        native_diff.staminaDifficulty = difficulty_attributes.stamina_difficulty
        native_diff.monoStaminaFactor = difficulty_attributes.mono_stamina_factor
        native_diff.consistencyFactor = difficulty_attributes.consistency_factor
        native_diff.staminaTopStrains = difficulty_attributes.stamina_top_strains

        native_perf = bindings.NativeTaikoPerformanceAttributes()
        result = bindings.TaikoPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        NativeHelper.check_error(result, "calculate Taiko performance")

        return TaikoPerformanceAttributes.from_native(native_perf)

    def close(self) -> None:
        if not self._closed:
            bindings.TaikoPerformanceCalculator_Destroy(self.handle)
            self._closed = True


class CatchPerformanceCalculator(PerformanceCalculator):
    @classmethod
    def create(cls) -> CatchPerformanceCalculator:
        native_calc = bindings.NativeCatchPerformanceCalculator()
        result = bindings.CatchPerformanceCalculator_Create(byref(native_calc))
        NativeHelper.check_error(result, "create CatchPerformanceCalculator")
        return cls(native_calc.handle)

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

        native_diff = bindings.NativeCatchDifficultyAttributes()
        native_diff.starRating = difficulty_attributes.star_rating
        native_diff.maxCombo = difficulty_attributes.max_combo

        native_perf = bindings.NativeCatchPerformanceAttributes()
        result = bindings.CatchPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        NativeHelper.check_error(result, "calculate Catch performance")

        return CatchPerformanceAttributes.from_native(native_perf)

    def close(self) -> None:
        if not self._closed:
            bindings.CatchPerformanceCalculator_Destroy(self.handle)
            self._closed = True


class ManiaPerformanceCalculator(PerformanceCalculator):
    @classmethod
    def create(cls) -> ManiaPerformanceCalculator:
        native_calc = bindings.NativeManiaPerformanceCalculator()
        result = bindings.ManiaPerformanceCalculator_Create(byref(native_calc))
        NativeHelper.check_error(result, "create ManiaPerformanceCalculator")
        return cls(native_calc.handle)

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

        native_diff = bindings.NativeManiaDifficultyAttributes()
        native_diff.starRating = difficulty_attributes.star_rating
        native_diff.maxCombo = difficulty_attributes.max_combo

        native_perf = bindings.NativeManiaPerformanceAttributes()
        result = bindings.ManiaPerformanceCalculator_Calculate(
            self.handle,
            native_score,
            native_diff,
            byref(native_perf),
        )
        NativeHelper.check_error(result, "calculate Mania performance")

        return ManiaPerformanceAttributes.from_native(native_perf)

    def close(self) -> None:
        if not self._closed:
            bindings.ManiaPerformanceCalculator_Destroy(self.handle)
            self._closed = True


def create_performance_calculator(ruleset: Ruleset) -> PerformanceCalculator:
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
