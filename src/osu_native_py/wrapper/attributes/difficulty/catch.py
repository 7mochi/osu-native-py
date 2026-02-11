from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeCatchDifficultyAttributes
from ....native import bindings
from .base import DifficultyAttributes


@dataclass
class CatchDifficultyAttributes(DifficultyAttributes):
    @classmethod
    def from_native(cls, native: NativeCatchDifficultyAttributes) -> CatchDifficultyAttributes:
        return cls(
            star_rating=native.starRating,
            max_combo=native.maxCombo,
        )
