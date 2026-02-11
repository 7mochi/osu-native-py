from __future__ import annotations

from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

BEATMAP_PATH = "/home/nanamochi/Descargas/1492006.osu"


with Beatmap.from_file(BEATMAP_PATH) as beatmap:
    with Ruleset.from_id(0) as ruleset:
        with ModsCollection.create() as mods:
            for mod_name in ["DT", "CL"]:
                mod = Mod.create(mod_name)
                mods.add(mod)
            mods.debug()

            score = ScoreInfo(
                accuracy=0.9436619718309859,
                max_combo=116,
                count_great=65,
                count_meh=0,
                count_ok=6,
                count_miss=0,
            )
            print(score)

            with create_difficulty_calculator(ruleset, beatmap) as diff_calc:
                diff_attrs = diff_calc.calculate(mods)

            with create_performance_calculator(ruleset) as perf_calc:
                perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)
                print(perf_attrs.total)
