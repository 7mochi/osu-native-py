from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PerformanceAttributes:
    """Base class for performance attributes.

    Attributes:
        total: The final calculated performance points.
    """

    total: float
