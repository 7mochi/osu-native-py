from __future__ import annotations

from pathlib import Path

import pytest

from osu_native_py.wrapper.attributes.difficulty.catch import CatchDifficultyAttributes
from osu_native_py.wrapper.attributes.performance.catch import CatchPerformanceAttributes
from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

TEST_DIR = Path(__file__).parent
BEATMAP_PATH = TEST_DIR / "resources/4289411.osu"


def test_standard_ruleset():
    beatmap = Beatmap.from_file(str(BEATMAP_PATH))
    ruleset = Ruleset.from_id(2)
    mods = ModsCollection.create()

    score = ScoreInfo(
        accuracy=1.0,
        max_combo=1909,
        count_great=1836,
        count_large_tick_hit=73,
        count_small_tick_hit=86,
    )

    diff_calc = create_difficulty_calculator(ruleset, beatmap)
    diff_attrs = diff_calc.calculate(mods)

    perf_calc = create_performance_calculator(ruleset)
    perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)

    if isinstance(diff_attrs, CatchDifficultyAttributes):
        assert diff_attrs.star_rating == pytest.approx(8.023384332389398)
        assert diff_attrs.max_combo == 1909

    if isinstance(perf_attrs, CatchPerformanceAttributes):
        assert perf_attrs.total == pytest.approx(852.7183421110947)
