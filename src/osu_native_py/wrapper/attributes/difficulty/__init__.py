from __future__ import annotations

from osu_native_py.native.attributes import TimedCatchDifficultyAttributes
from osu_native_py.native.attributes import TimedManiaDifficultyAttributes
from osu_native_py.native.attributes import TimedOsuDifficultyAttributes
from osu_native_py.native.attributes import TimedTaikoDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.base import DifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.catch import CatchDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.mania import ManiaDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.osu import OsuDifficultyAttributes
from osu_native_py.wrapper.attributes.difficulty.taiko import TaikoDifficultyAttributes

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
