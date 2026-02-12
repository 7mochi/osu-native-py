from __future__ import annotations

from ctypes import byref
from typing import Optional

from ...native import ManagedObjectHandle
from ...native import NativeBeatmap
from ...native import bindings
from ..utils.native_handler import NativeHandler
from .error_code import ErrorCode


class Beatmap(NativeHandler):
    def __init__(self, native_beatmap: NativeBeatmap):
        super().__init__(native_beatmap)

    @classmethod
    def from_file(cls, file_path: str) -> Beatmap:
        native_string = cls.create_native_string(file_path)
        native_beatmap = bindings.NativeBeatmap()

        result = bindings.Beatmap_CreateFromFile(native_string, byref(native_beatmap))
        cls.check_error(result, f"create beatmap from file '{file_path}'")

        return cls(native_beatmap)

    @classmethod
    def from_text(cls, beatmap_text: str) -> Beatmap:
        native_string = cls.create_native_string(beatmap_text)
        native_beatmap = bindings.NativeBeatmap()

        result = bindings.Beatmap_CreateFromText(native_string, byref(native_beatmap))
        cls.check_error(result, "create beatmap from text")

        return cls(native_beatmap)

    @property
    def title(self) -> str:
        self._check_not_closed()
        return self.get_string(bindings.Beatmap_GetTitle)

    @property
    def artist(self) -> str:
        self._check_not_closed()
        return self.get_string(bindings.Beatmap_GetArtist)

    @property
    def version(self) -> str:
        self._check_not_closed()
        return self.get_string(bindings.Beatmap_GetVersion)

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

    def _destroy(self) -> None:
        bindings.Beatmap_Destroy(self.handle)

    def __repr__(self) -> str:
        if self.is_closed:
            return f"<Beatmap (closed)>"

        try:
            return (
                f"<Beatmap '{self.artist} - {self.title} [{self.version}]' "
                f"AR={self.approach_rate:.1f} OD={self.overall_difficulty:.1f}>"
            )
        except:
            return f"<Beatmap handle={self.handle.id}>"
