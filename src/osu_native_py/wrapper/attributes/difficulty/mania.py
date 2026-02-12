from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeManiaDifficultyAttributes
from .base import DifficultyAttributes


@dataclass
class ManiaDifficultyAttributes(DifficultyAttributes):
    @classmethod
    def from_native(cls, native: NativeManiaDifficultyAttributes) -> ManiaDifficultyAttributes:
        return cls(
            star_rating=native.starRating,
            max_combo=native.maxCombo,
        )
