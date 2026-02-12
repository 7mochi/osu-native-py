from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeOsuDifficultyAttributes
from .base import DifficultyAttributes


@dataclass
class OsuDifficultyAttributes(DifficultyAttributes):
    """Difficulty attributes for osu!standard mode.

    Attributes:
        aim_difficulty: The difficulty corresponding to the aim skill.
        aim_difficult_slider_count: The number of sliders weighted by difficulty.
        speed_difficulty: The difficulty corresponding to the speed skill.
        speed_note_count: The number of clickable objects weighted by difficulty.
            Related to speed_difficulty.
        flashlight_difficulty: The difficulty corresponding to the flashlight skill.
        slider_factor: Describes how much of aim_difficulty is contributed by
            hitcircles or sliders. A value closer to 1.0 indicates most of
            aim_difficulty is contributed by hitcircles. A value closer to 0.0
            indicates most of aim_difficulty is contributed by sliders.
        aim_top_weighted_slider_factor: Describes how much of aim_difficult_strain_count
            is contributed by hitcircles or sliders. A value closer to 0.0 indicates
            most is contributed by hitcircles. A value closer to infinity indicates
            most is contributed by sliders.
        speed_top_weighted_slider_factor: Describes how much of
            speed_difficult_strain_count is contributed by hitcircles or sliders.
            A value closer to 0.0 indicates most is contributed by hitcircles.
            A value closer to infinity indicates most is contributed by sliders.
        aim_difficult_strain_count: The count of difficult aim strains.
        speed_difficult_strain_count: The count of difficult speed strains.
        nested_score_per_object: The nested score per object.
        legacy_score_base_multiplier: The base multiplier for legacy scoring.
        maximum_legacy_combo_score: The maximum legacy combo score.
        drain_rate: The beatmap's drain rate. This doesn't scale with
            rate-adjusting mods.
        hit_circle_count: The number of hitcircles in the beatmap.
        slider_count: The number of sliders in the beatmap.
        spinner_count: The number of spinners in the beatmap.
    """

    aim_difficulty: float
    aim_difficult_slider_count: float
    speed_difficulty: float
    speed_note_count: float
    flashlight_difficulty: float
    slider_factor: float
    aim_top_weighted_slider_factor: float
    speed_top_weighted_slider_factor: float
    aim_difficult_strain_count: float
    speed_difficult_strain_count: float
    nested_score_per_object: float
    legacy_score_base_multiplier: float
    maximum_legacy_combo_score: float
    drain_rate: float
    hit_circle_count: int
    slider_count: int
    spinner_count: int

    @classmethod
    def from_native(cls, native: NativeOsuDifficultyAttributes) -> OsuDifficultyAttributes:
        return cls(
            star_rating=native.starRating,
            max_combo=native.maxCombo,
            aim_difficulty=native.aimDifficulty,
            aim_difficult_slider_count=native.aimDifficultSliderCount,
            speed_difficulty=native.speedDifficulty,
            speed_note_count=native.speedNoteCount,
            flashlight_difficulty=native.flashlightDifficulty,
            slider_factor=native.sliderFactor,
            aim_top_weighted_slider_factor=native.aimTopWeightedSliderFactor,
            speed_top_weighted_slider_factor=native.speedTopWeightedSliderFactor,
            aim_difficult_strain_count=native.aimDifficultStrainCount,
            speed_difficult_strain_count=native.speedDifficultStrainCount,
            nested_score_per_object=native.nestedScorePerObject,
            legacy_score_base_multiplier=native.legacyScoreBaseMultiplier,
            maximum_legacy_combo_score=native.maximumLegacyComboScore,
            drain_rate=native.drainRate,
            hit_circle_count=native.hitCircleCount,
            slider_count=native.sliderCount,
            spinner_count=native.spinnerCount,
        )
