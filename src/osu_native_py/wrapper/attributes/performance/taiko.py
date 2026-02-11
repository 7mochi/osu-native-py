from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ....native import NativeTaikoPerformanceAttributes
from ....native import bindings
from .base import PerformanceAttributes


@dataclass
class TaikoPerformanceAttributes(PerformanceAttributes):
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
