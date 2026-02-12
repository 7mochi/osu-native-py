from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DifficultyAttributes:
    """Base class for difficulty attributes.

    Contains the difficulty of a beatmap, as output by a difficulty calculator.

    Attributes:
        star_rating: The combined star rating of all skills.
        max_combo: The maximum achievable combo.
    """

    star_rating: float
    max_combo: int
