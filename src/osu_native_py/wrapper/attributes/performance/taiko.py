from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ....native import NativeTaikoPerformanceAttributes
from .base import PerformanceAttributes


@dataclass
class TaikoPerformanceAttributes(PerformanceAttributes):
    """Performance attributes for osu!taiko mode.

    Attributes:
        difficulty: The difficulty portion of the final performance points.
        accuracy: The accuracy portion of the final performance points.
        estimated_unstable_rate: Approximated unstable rate. None if not available.
    """

    difficulty: float
    accuracy: float
    estimated_unstable_rate: Optional[float]

    @classmethod
    def from_native(cls, native: NativeTaikoPerformanceAttributes) -> TaikoPerformanceAttributes:
        return cls(
            total=native.total,
            difficulty=native.difficulty,
            accuracy=native.accuracy,
            estimated_unstable_rate=(
                native.estimatedUnstableRate.value
                if native.estimatedUnstableRate.hasValue
                else None
            ),
        )
