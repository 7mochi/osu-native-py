from __future__ import annotations

from .base import DifficultyAttributes
from .catch import CatchDifficultyAttributes
from .mania import ManiaDifficultyAttributes
from .osu import OsuDifficultyAttributes
from .taiko import TaikoDifficultyAttributes

__all__ = [
    "DifficultyAttributes",
    "OsuDifficultyAttributes",
    "TaikoDifficultyAttributes",
    "CatchDifficultyAttributes",
    "ManiaDifficultyAttributes",
]
