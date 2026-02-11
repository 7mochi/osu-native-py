"""Wrapper de alto nivel para osu-native-py."""

# Solo re-exportamos los submódulos, no las clases individuales
# Los usuarios deben usar imports explícitos: from osu_native_py.wrapper.objects import Beatmap
from __future__ import annotations

from . import attributes
from . import calculators
from . import objects

__all__ = [
    "objects",
    "attributes",
    "calculators",
]
