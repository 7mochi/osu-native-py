from __future__ import annotations

from osu_native_py.wrapper.attributes.performance.base import PerformanceAttributes
from osu_native_py.wrapper.attributes.performance.catch import CatchPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.mania import ManiaPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.osu import OsuPerformanceAttributes
from osu_native_py.wrapper.attributes.performance.taiko import TaikoPerformanceAttributes

__all__ = [
    "PerformanceAttributes",
    "OsuPerformanceAttributes",
    "TaikoPerformanceAttributes",
    "CatchPerformanceAttributes",
    "ManiaPerformanceAttributes",
]
