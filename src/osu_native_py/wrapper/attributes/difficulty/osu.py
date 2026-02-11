from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeOsuDifficultyAttributes
from ....native import bindings
from .base import DifficultyAttributes


@dataclass
class OsuDifficultyAttributes(DifficultyAttributes):
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
