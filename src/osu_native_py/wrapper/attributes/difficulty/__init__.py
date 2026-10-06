from __future__ import annotations

from ....native.attributes import TimedCatchDifficultyAttributes
from ....native.attributes import TimedManiaDifficultyAttributes
from ....native.attributes import TimedOsuDifficultyAttributes
from ....native.attributes import TimedTaikoDifficultyAttributes
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
    "TimedOsuDifficultyAttributes",
    "TimedTaikoDifficultyAttributes",
    "TimedCatchDifficultyAttributes",
    "TimedManiaDifficultyAttributes",
]
