from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DifficultyAttributes:
    star_rating: float
    max_combo: int
