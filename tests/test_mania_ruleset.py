from __future__ import annotations

from pathlib import Path

import pytest

from osu_native_py.wrapper.attributes.difficulty.mania import ManiaDifficultyAttributes
from osu_native_py.wrapper.attributes.performance.mania import ManiaPerformanceAttributes
from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

TEST_DIR = Path(__file__).parent
BEATMAP_PATH = TEST_DIR / "resources/5107047.osu"


def test_standard_ruleset():
    beatmap = Beatmap.from_file(str(BEATMAP_PATH))
    ruleset = Ruleset.from_id(2)
    mods = ModsCollection.create()

    score = ScoreInfo(
        accuracy=0.9779,
        max_combo=2142,
        count_perfect=18261,
        count_great=6214,
        count_good=562,
        count_ok=113,
        count_meh=73,
        count_miss=127,
    )

    diff_calc = create_difficulty_calculator(ruleset, beatmap)
    diff_attrs = diff_calc.calculate(mods)

    perf_calc = create_performance_calculator(ruleset)
    perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)

    if isinstance(diff_attrs, ManiaDifficultyAttributes):
        assert diff_attrs.star_rating == pytest.approx(11.627630733008322)
        assert diff_attrs.max_combo == 24779

    if isinstance(perf_attrs, ManiaPerformanceAttributes):
        assert perf_attrs.total == pytest.approx(1566.2954965275737)
        assert perf_attrs.difficulty == pytest.approx(1566.2954965275737)
