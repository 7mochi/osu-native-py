from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ...native import ManagedObjectHandle
from ...native import NativeScoreInfo
from ...native import bindings


@dataclass
class ScoreInfo:
    max_combo: int = 0
    accuracy: float = 1.0
    count_miss: int = 0
    count_meh: int = 0
    count_ok: int = 0
    count_good: int = 0
    count_great: int = 0
    count_perfect: int = 0
    count_slider_tail_hit: int = 0
    count_large_tick_miss: int = 0
    legacy_total_score: Optional[int] = None

    def to_native(
        self,
        ruleset_handle: ManagedObjectHandle,
        beatmap_handle: ManagedObjectHandle,
        mods_handle: ManagedObjectHandle,
    ) -> NativeScoreInfo:
        native_score = bindings.NativeScoreInfo()
        native_score.rulesetHandle = ruleset_handle
        native_score.beatmapHandle = beatmap_handle
        native_score.modsHandle = mods_handle
        native_score.maxCombo = self.max_combo
        native_score.accuracy = self.accuracy

        if self.legacy_total_score is not None:
            native_score.legacyTotalScore.hasValue = True
            native_score.legacyTotalScore.value = self.legacy_total_score
        else:
            native_score.legacyTotalScore.hasValue = False
            native_score.legacyTotalScore.value = 0

        native_score.countMiss = self.count_miss
        native_score.countMeh = self.count_meh
        native_score.countOk = self.count_ok
        native_score.countGood = self.count_good
        native_score.countGreat = self.count_great
        native_score.countPerfect = self.count_perfect
        native_score.countSliderTailHit = self.count_slider_tail_hit
        native_score.countLargeTickMiss = self.count_large_tick_miss

        return native_score
