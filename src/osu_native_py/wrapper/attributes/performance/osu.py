from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ....native import NativeOsuPerformanceAttributes
from .base import PerformanceAttributes


@dataclass
class OsuPerformanceAttributes(PerformanceAttributes):
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
