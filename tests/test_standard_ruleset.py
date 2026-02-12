from __future__ import annotations

from pathlib import Path

import pytest

from osu_native_py.wrapper.attributes.difficulty.osu import OsuDifficultyAttributes
from osu_native_py.wrapper.attributes.performance.osu import OsuPerformanceAttributes
from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

TEST_DIR = Path(__file__).parent
BEATMAP_PATH = TEST_DIR / "resources/5438072.osu"


def test_standard_ruleset():
    beatmap = Beatmap.from_file(str(BEATMAP_PATH))
    ruleset = Ruleset.from_id(0)
    mods = ModsCollection.create()

    for mod_name in ["HD", "DT"]:
        mod = Mod.create(mod_name)
        mods.add(mod)

    score = ScoreInfo(accuracy=1.0, max_combo=183, count_great=140, count_slider_tail_hit=43)

    diff_calc = create_difficulty_calculator(ruleset, beatmap)
    diff_attrs = diff_calc.calculate(mods)

    perf_calc = create_performance_calculator(ruleset)
    perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)

    if isinstance(diff_attrs, OsuDifficultyAttributes):
        assert diff_attrs.star_rating == pytest.approx(7.765762362059099)
        assert diff_attrs.max_combo == 183
        assert diff_attrs.aim_difficulty == pytest.approx(4.3682123359710925)
        assert diff_attrs.aim_difficult_slider_count == pytest.approx(22.686766833130047)
        assert diff_attrs.speed_difficulty == pytest.approx(2.8560898921433444)
        assert diff_attrs.speed_note_count == pytest.approx(113.75894687178317)
        assert diff_attrs.slider_factor == pytest.approx(0.9943922184830679)
        assert diff_attrs.aim_top_weighted_slider_factor == pytest.approx(0.3840426059241585)
        assert diff_attrs.speed_top_weighted_slider_factor == pytest.approx(0.4713024554831769)
        assert diff_attrs.aim_difficult_strain_count == pytest.approx(46.199831564028564)
        assert diff_attrs.speed_difficult_strain_count == pytest.approx(60.800851497024794)
        assert diff_attrs.nested_score_per_object == pytest.approx(18.428571428571427)
        assert diff_attrs.legacy_score_base_multiplier == 4
        assert diff_attrs.maximum_legacy_combo_score == 615888

    if isinstance(perf_attrs, OsuPerformanceAttributes):
        assert perf_attrs.aim == pytest.approx(319.18472409411135)
        assert perf_attrs.total == pytest.approx(563.1769678409995)
        assert perf_attrs.speed == pytest.approx(87.45481790157747)
        assert perf_attrs.accuracy == pytest.approx(131.2126708522303)
        assert perf_attrs.flashlight == pytest.approx(0.0)
        assert perf_attrs.effective_miss_count == pytest.approx(0.0)
        assert perf_attrs.speed_deviation == pytest.approx(8.46064257633682)
        assert perf_attrs.combo_based_estimated_miss_count == pytest.approx(0.0)
        assert perf_attrs.score_based_estimated_miss_count == pytest.approx(0.0)
        assert perf_attrs.aim_estimated_slider_breaks == pytest.approx(0.0)
        assert perf_attrs.speed_estimated_slider_breaks == pytest.approx(0.0)
