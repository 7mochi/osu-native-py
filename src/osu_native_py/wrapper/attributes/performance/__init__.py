from __future__ import annotations

from .base import PerformanceAttributes
from .catch import CatchPerformanceAttributes
from .mania import ManiaPerformanceAttributes
from .osu import OsuPerformanceAttributes
from .taiko import TaikoPerformanceAttributes

__all__ = [
    "PerformanceAttributes",
    "OsuPerformanceAttributes",
    "TaikoPerformanceAttributes",
    "CatchPerformanceAttributes",
    "ManiaPerformanceAttributes",
]
