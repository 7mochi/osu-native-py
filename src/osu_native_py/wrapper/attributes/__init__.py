from __future__ import annotations

from osu_native_py.wrapper.attributes.difficulty import TimedCatchDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty import TimedManiaDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty import TimedOsuDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty import TimedTaikoDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.base import DifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.catch import CatchDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.mania import ManiaDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.osu import OsuDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.taiko import TaikoDifficultyAttributes
from osu_native_py.wrapper.attributes.performance.base import PerformanceAttributes
from osu_native_py.wrapper.attributes.performance.catch import CatchPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.mania import ManiaPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.osu import OsuPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.taiko import TaikoPerformanceAttributes

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
    "PerformanceAttributes",
    "OsuPerformanceAttributes",
    "TaikoPerformanceAttributes",
    "CatchPerformanceAttributes",
    "ManiaPerformanceAttributes",
]
