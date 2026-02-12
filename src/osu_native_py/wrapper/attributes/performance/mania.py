from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeManiaPerformanceAttributes
from .base import PerformanceAttributes


@dataclass
class ManiaPerformanceAttributes(PerformanceAttributes):
    """Performance attributes for osu!mania mode.

    Attributes:
        difficulty: The difficulty portion of the final performance points.
    """

    difficulty: float

    @classmethod
    def from_native(cls, native: NativeManiaPerformanceAttributes) -> ManiaPerformanceAttributes:
        return cls(
            total=native.total,
            difficulty=native.difficulty,
        )
