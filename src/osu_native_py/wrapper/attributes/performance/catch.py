from __future__ import annotations

from dataclasses import dataclass

from ....native import NativeCatchPerformanceAttributes
from .base import PerformanceAttributes


@dataclass
class CatchPerformanceAttributes(PerformanceAttributes):
    @classmethod
    def from_native(cls, native: NativeCatchPerformanceAttributes) -> CatchPerformanceAttributes:
        return cls(total=native.total)
