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
        assert diff_attrs.star_rating == pytest.approx(5.826375388637023)
        assert diff_attrs.max_combo == 453
        assert diff_attrs.mechanical_difficulty == pytest.approx(4.362772590460359)
        assert diff_attrs.rhythm_difficulty == pytest.approx(1.4625032919966257)
        assert diff_attrs.reading_difficulty == pytest.approx(0.0010995061800368473)
        assert diff_attrs.colour_difficulty == pytest.approx(1.2796371462388172)
        assert diff_attrs.stamina_difficulty == pytest.approx(3.083135444221542)
        assert diff_attrs.mono_stamina_factor == pytest.approx(1.8585410552067942e-08, abs=1e-15)
        assert diff_attrs.consistency_factor == pytest.approx(0.7117837850730536)
        assert diff_attrs.stamina_top_strains == pytest.approx(125.66323763031244)

    if isinstance(perf_attrs, TaikoPerformanceAttributes):
        assert perf_attrs.total == pytest.approx(437.12346889778064)
        assert perf_attrs.difficulty == pytest.approx(240.57633493439914)
        assert perf_attrs.accuracy == pytest.approx(196.5471339633815)
        assert perf_attrs.estimated_unstable_rate == pytest.approx(91.33286105656317)
