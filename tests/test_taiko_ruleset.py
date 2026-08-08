from __future__ import annotations

from pathlib import Path

import pytest

from osu_native_py.wrapper.attributes.difficulty.taiko import TaikoDifficultyAttributes
from osu_native_py.wrapper.attributes.performance.taiko import TaikoPerformanceAttributes
from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

TEST_DIR = Path(__file__).parent
BEATMAP_PATH = TEST_DIR / "resources/221923.osu"


def test_standard_ruleset():
    beatmap = Beatmap.from_file(str(BEATMAP_PATH))
    ruleset = Ruleset.from_id(1)
    mods = ModsCollection.create()

    for mod_name in ["DT"]:
        mod = Mod.create(mod_name)
        mods.add(mod)

    score = ScoreInfo(accuracy=1.0, max_combo=453, count_great=453)

    diff_calc = create_difficulty_calculator(ruleset, beatmap)
    diff_attrs = diff_calc.calculate(mods)

    perf_calc = create_performance_calculator(ruleset)
    perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)

    if isinstance(diff_attrs, TaikoDifficultyAttributes):
        assert diff_attrs.star_rating == pytest.approx(5.776751574977793)
        assert diff_attrs.max_combo == 453
        assert diff_attrs.mechanical_difficulty == pytest.approx(4.575263019721287)
        assert diff_attrs.rhythm_difficulty == pytest.approx(1.2003354972271978)
        assert diff_attrs.reading_difficulty == pytest.approx(0.0011530580293085551)
        assert diff_attrs.colour_difficulty == pytest.approx(1.3419623398776226)
        assert diff_attrs.stamina_difficulty == pytest.approx(3.2333006798436643)
        assert diff_attrs.mono_stamina_factor == pytest.approx(1.8585410552067947e-08, abs=1e-15)
        assert diff_attrs.consistency_factor == pytest.approx(0.7002259535141709)
        assert diff_attrs.stamina_top_strains == pytest.approx(125.66323763031251)

    if isinstance(perf_attrs, TaikoPerformanceAttributes):
        assert perf_attrs.total == pytest.approx(432.0844637877409)
        assert perf_attrs.difficulty == pytest.approx(235.90400271061765)
        assert perf_attrs.accuracy == pytest.approx(196.18046107712328)
        assert perf_attrs.estimated_unstable_rate == pytest.approx(91.33286105656319)
