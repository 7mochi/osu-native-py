from __future__ import annotations

from .difficulty.base import DifficultyAttributes
from .difficulty.catch import CatchDifficultyAttributes
from .difficulty.mania import ManiaDifficultyAttributes
from .difficulty.osu import OsuDifficultyAttributes
from .difficulty.taiko import TaikoDifficultyAttributes
from .performance.base import PerformanceAttributes
from .performance.catch import CatchPerformanceAttributes
from .performance.mania import ManiaPerformanceAttributes
from .performance.osu import OsuPerformanceAttributes
from .performance.taiko import TaikoPerformanceAttributes

__all__ = [
    "DifficultyAttributes",
    "OsuDifficultyAttributes",
    "TaikoDifficultyAttributes",
    "CatchDifficultyAttributes",
    "ManiaDifficultyAttributes",
    "PerformanceAttributes",
    "OsuPerformanceAttributes",
    "TaikoPerformanceAttributes",
    "CatchPerformanceAttributes",
    "ManiaPerformanceAttributes",
]
