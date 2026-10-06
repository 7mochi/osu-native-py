from __future__ import annotations

import json
from contextlib import ExitStack
from dataclasses import asdict
from pathlib import Path

import pytest

from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "osu-native/osu.Native.Tests/Resources"
CASES = [
    case
    for filename in ("difficulty.json", "timed-difficulty.json", "performance.json")
    for case in json.loads((ROOT / "build/generated" / filename).read_text(encoding="utf-8"))
]


@pytest.mark.parametrize("case", CASES)
def test_calculator(case):
    with ExitStack() as stack:
        beatmap = stack.enter_context(Beatmap.from_file(str(RESOURCES / case["beatmap"])))
        ruleset = stack.enter_context(Ruleset.from_id(case["ruleset"]))
        mods = stack.enter_context(ModsCollection.create())
        for entry in case["mods"]:
            mod = stack.enter_context(Mod.create(entry["acronym"]))
            setters = {
                bool: mod.set_setting_bool,
                int: mod.set_setting_int,
                float: mod.set_setting_float,
            }
            for key, value in entry.get("settings", {}).items():
                setters[type(value)](key, value)
            mods.add(mod)

        difficulty = stack.enter_context(create_difficulty_calculator(ruleset, beatmap))
        if "index" in case:
            actual = difficulty.calculate_timed(mods)[case["index"]]
        else:
            actual = difficulty.calculate(mods)
            if "score" in case:
                performance = stack.enter_context(create_performance_calculator(ruleset))
                actual = performance.calculate(
                    ruleset,
                    beatmap,
                    mods,
                    ScoreInfo(**case["score"]),
                    actual,
                )

        assert_attributes(asdict(actual), case["expected"])


def assert_attributes(actual, expected):
    assert actual.keys() == expected.keys()
    for name, value in actual.items():
        if isinstance(value, dict):
            assert_attributes(value, expected[name])
        elif isinstance(value, float) and expected[name] is not None:
            assert value == pytest.approx(expected[name], rel=0, abs=0.00001), name
        else:
            assert value == expected[name], name
