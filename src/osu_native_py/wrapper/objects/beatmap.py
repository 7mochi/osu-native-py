from __future__ import annotations

from ctypes import byref
from typing import Optional

from ...native import ManagedObjectHandle
from ...native import NativeBeatmap
from ...native import bindings
from .error_code import ErrorCode
from .native_helper import NativeHelper


class Beatmap:
    def __init__(self, native_beatmap: NativeBeatmap):
        self._native = native_beatmap
        self._closed = False

    @classmethod
    def from_file(cls, file_path: str) -> Beatmap:
        native_string = NativeHelper.create_native_string(file_path)
        native_beatmap = bindings.NativeBeatmap()

        result = bindings.Beatmap_CreateFromFile(native_string, byref(native_beatmap))
        NativeHelper.check_error(result, f"create beatmap from file '{file_path}'")

        return cls(native_beatmap)

    @classmethod
    def from_text(cls, beatmap_text: str) -> Beatmap:
        native_string = NativeHelper.create_native_string(beatmap_text)
        native_beatmap = bindings.NativeBeatmap()

        result = bindings.Beatmap_CreateFromText(native_string, byref(native_beatmap))
        NativeHelper.check_error(result, "create beatmap from text")

        return cls(native_beatmap)

    @property
    def handle(self) -> ManagedObjectHandle:
        return self._native.handle

    @property
    def title(self) -> str:
        self._check_not_closed()
        return NativeHelper.get_string(self.handle, bindings.Beatmap_GetTitle)

    @property
    def artist(self) -> str:
        self._check_not_closed()
        return NativeHelper.get_string(self.handle, bindings.Beatmap_GetArtist)

    @property
    def version(self) -> str:
        self._check_not_closed()
        return NativeHelper.get_string(self.handle, bindings.Beatmap_GetVersion)

    @property
    def approach_rate(self) -> float:
        self._check_not_closed()
        return self._native.approachRate

    @property
    def drain_rate(self) -> float:
        self._check_not_closed()
        return self._native.drainRate

    @property
    def overall_difficulty(self) -> float:
        self._check_not_closed()
        return self._native.overallDifficulty

    @property
    def circle_size(self) -> float:
        self._check_not_closed()
        return self._native.circleSize

    @property
    def slider_multiplier(self) -> float:
        self._check_not_closed()
        return self._native.sliderMultiplier

    @property
    def slider_tick_rate(self) -> float:
        self._check_not_closed()
        return self._native.sliderTickRate

    @property
    def ruleset_id(self) -> int:
        self._check_not_closed()
        return self._native.rulesetId

    @property
    def beatmap_id(self) -> int:
        self._check_not_closed()
        return self._native.beatmapId

    @property
    def is_closed(self) -> bool:
        return self._closed

    def _check_not_closed(self) -> None:
        if self._closed:
            raise RuntimeError("Beatmap has been closed")

    def close(self) -> None:
        if not self._closed:
            bindings.Beatmap_Destroy(self.handle)
            self._closed = True

    def __enter__(self) -> Beatmap:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        if not self._closed:
            self.close()

    def __repr__(self) -> str:
        if self._closed:
            return f"<Beatmap (closed)>"
        try:
            return (
                f"<Beatmap '{self.artist} - {self.title} [{self.version}]' "
                f"AR={self.approach_rate:.1f} OD={self.overall_difficulty:.1f}>"
            )
        except:
            return f"<Beatmap handle={self.handle.id}>"
