from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ....native import NativeOsuPerformanceAttributes
from .base import PerformanceAttributes


@dataclass
class OsuPerformanceAttributes(PerformanceAttributes):
    """Performance attributes for osu!standard mode.

    Attributes:
        aim: The aim portion of the final performance points.
        speed: The speed portion of the final performance points.
        accuracy: The accuracy portion of the final performance points.
        flashlight: The flashlight portion of the final performance points.
        effective_miss_count: Misses including an approximated amount of
            slider breaks.
        speed_deviation: Approximated unstable rate. None if not available.
        combo_based_estimated_miss_count: Estimated miss count based on the
            player's combo.
        score_based_estimated_miss_count: Estimated miss count based on the
            player's score. None if not available.
        aim_estimated_slider_breaks: Estimated number of slider breaks that
            affected the aim portion.
        speed_estimated_slider_breaks: Estimated number of slider breaks that
            affected the speed portion.
    """

    aim: float
    speed: float
    accuracy: float
    flashlight: float
    effective_miss_count: float
    speed_deviation: Optional[float]
    combo_based_estimated_miss_count: float
    score_based_estimated_miss_count: Optional[float]
    aim_estimated_slider_breaks: float
    speed_estimated_slider_breaks: float

    @classmethod
    def from_native(cls, native: NativeOsuPerformanceAttributes) -> OsuPerformanceAttributes:
        return cls(
            total=native.total,
            aim=native.aim,
            speed=native.speed,
            accuracy=native.accuracy,
            flashlight=native.flashlight,
            effective_miss_count=native.effectiveMissCount,
            speed_deviation=native.speedDeviation.value if native.speedDeviation.hasValue else None,
            combo_based_estimated_miss_count=native.comboBasedEstimatedMissCount,
            score_based_estimated_miss_count=(
                native.scoreBasedEstimatedMissCount.value
                if native.scoreBasedEstimatedMissCount.hasValue
                else None
            ),
            aim_estimated_slider_breaks=native.aimEstimatedSliderBreaks,
            speed_estimated_slider_breaks=native.speedEstimatedSliderBreaks,
        )
