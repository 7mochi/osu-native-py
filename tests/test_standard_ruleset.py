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
        assert diff_attrs.star_rating == pytest.approx(7.498739590295447)
        assert diff_attrs.max_combo == 183
        assert diff_attrs.aim_difficulty == pytest.approx(4.357329621795068)
        assert diff_attrs.aim_difficult_slider_count == pytest.approx(30.345999170641857)
        assert diff_attrs.speed_difficulty == pytest.approx(2.0211429286638367)
        assert diff_attrs.speed_note_count == pytest.approx(120.07110728462541)
        assert diff_attrs.reading_difficulty == pytest.approx(1.9730918640558355)
        assert diff_attrs.slider_factor == pytest.approx(0.9906160459443888)
        assert diff_attrs.aim_top_weighted_slider_factor == pytest.approx(0.41441635619904416)
        assert diff_attrs.speed_top_weighted_slider_factor == pytest.approx(0.45254841769401155)
        assert diff_attrs.aim_difficult_strain_count == pytest.approx(58.35038516550769)
        assert diff_attrs.speed_difficult_strain_count == pytest.approx(62.04319093927151)
        assert diff_attrs.reading_difficult_note_count == pytest.approx(37.73907995641551)
        assert diff_attrs.nested_score_per_object == pytest.approx(18.428571428571427)
        assert diff_attrs.legacy_score_base_multiplier == 4
        assert diff_attrs.maximum_legacy_combo_score == 615888

    if isinstance(perf_attrs, OsuPerformanceAttributes):
        assert perf_attrs.aim == pytest.approx(322.4802177547998)
        assert perf_attrs.total == pytest.approx(524.5147724726088)
        assert perf_attrs.speed == pytest.approx(33.02442207926298)
        assert perf_attrs.accuracy == pytest.approx(124.35910173544602)
        assert perf_attrs.flashlight == pytest.approx(0.0)
        assert perf_attrs.reading == pytest.approx(30.725708690295477)
        assert perf_attrs.effective_miss_count == pytest.approx(0.0)
        assert perf_attrs.speed_deviation == pytest.approx(8.381088084982773)
        assert perf_attrs.combo_based_estimated_miss_count == pytest.approx(0.0)
        assert (
            perf_attrs.score_based_estimated_miss_count is None
            or perf_attrs.score_based_estimated_miss_count == pytest.approx(0.0)
        )
        assert perf_attrs.aim_estimated_slider_breaks == pytest.approx(0.0)
        assert perf_attrs.speed_estimated_slider_breaks == pytest.approx(0.0)
