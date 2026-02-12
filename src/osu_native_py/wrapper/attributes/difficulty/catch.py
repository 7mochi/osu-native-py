from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeCatchDifficultyAttributes
from .base import DifficultyAttributes


@dataclass
class CatchDifficultyAttributes(DifficultyAttributes):
    """Difficulty attributes for osu!catch mode.

    This class currently has no additional attributes beyond the base class.
    """

    @classmethod
    def from_native(cls, native: NativeCatchDifficultyAttributes) -> CatchDifficultyAttributes:
        return cls(
            star_rating=native.starRating,
            max_combo=native.maxCombo,
        )
