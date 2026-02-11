from __future__ import annotations

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    LIB_NAME = "osu.Native.dll"
    PLATFORM_DIR = "win-x64"
elif sys.platform == "darwin":
    LIB_NAME = "osu.Native.dylib"
    PLATFORM_DIR = "osx-x64"
else:
    LIB_NAME = "osu.Native.so"
    PLATFORM_DIR = "linux-x64"

BIN_DIR = Path(__file__).parent / "bin" / PLATFORM_DIR
LIB_PATH = BIN_DIR / LIB_NAME

if not BIN_DIR.exists():
    raise ImportError(
        f"Native library directory not found: {BIN_DIR}\n"
        f"Expected platform: {PLATFORM_DIR}\n"
        f"This package requires platform-specific native libraries.",
    )

if not LIB_PATH.exists():
    raise ImportError(
        f"Native library not found: {LIB_PATH}\n"
        f"Expected library: {LIB_NAME}\n"
        f"Available files in {BIN_DIR}: {list(BIN_DIR.iterdir()) if BIN_DIR.exists() else 'directory does not exist'}",
    )

os.environ.setdefault("OSUPY_LIBRARY_PATH", str(BIN_DIR))

from . import bindings

ManagedObjectHandle = bindings.ManagedObjectHandle

NativeBeatmap = bindings.NativeBeatmap
NativeMod = bindings.NativeMod
NativeModsCollection = bindings.NativeModsCollection
NativeRuleset = bindings.NativeRuleset
NativeScoreInfo = bindings.NativeScoreInfo

NativeOsuDifficultyAttributes = bindings.NativeOsuDifficultyAttributes
NativeTaikoDifficultyAttributes = bindings.NativeTaikoDifficultyAttributes
NativeCatchDifficultyAttributes = bindings.NativeCatchDifficultyAttributes
NativeManiaDifficultyAttributes = bindings.NativeManiaDifficultyAttributes

NativeOsuPerformanceAttributes = bindings.NativeOsuPerformanceAttributes
NativeTaikoPerformanceAttributes = bindings.NativeTaikoPerformanceAttributes
NativeCatchPerformanceAttributes = bindings.NativeCatchPerformanceAttributes
NativeManiaPerformanceAttributes = bindings.NativeManiaPerformanceAttributes

lib_handle = bindings._libs.get(LIB_NAME)
if lib_handle is None:
    available = list(bindings._libs.keys())
    raise ImportError(
        f"Failed to load {LIB_NAME} from {BIN_DIR}\n"
        f"Available libraries: {available}\n"
        f"This might indicate an incompatible binary or missing dependencies.",
    )

__all__ = [
    "LIB_NAME",
    "PLATFORM_DIR",
    "LIB_PATH",
    "BIN_DIR",
    "ManagedObjectHandle",
    "NativeBeatmap",
    "NativeMod",
    "NativeModsCollection",
    "NativeRuleset",
    "NativeScoreInfo",
    "NativeOsuDifficultyAttributes",
    "NativeTaikoDifficultyAttributes",
    "NativeCatchDifficultyAttributes",
    "NativeManiaDifficultyAttributes",
    "NativeOsuPerformanceAttributes",
    "NativeTaikoPerformanceAttributes",
    "NativeCatchPerformanceAttributes",
    "NativeManiaPerformanceAttributes",
]
