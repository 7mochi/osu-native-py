from __future__ import annotations

from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset


def test_ruleset():
    with Ruleset.from_id(0) as osu:
        assert osu.ruleset_id == 0
        assert osu.short_name == "osu"
        assert not osu.is_closed
        assert str(osu) == "Ruleset{rulesetId=0, shortName='osu'}"

    assert osu.is_closed

    with Ruleset.from_id(1) as taiko:
        assert taiko.ruleset_id == 1
        assert taiko.short_name == "taiko"

    with Ruleset.from_id(2) as catch:
        assert catch.ruleset_id == 2
        assert catch.short_name == "catch"

    with Ruleset.from_id(3) as mania:
        assert mania.ruleset_id == 3
        assert mania.short_name == "mania"


def test_mod():
    with Mod.create("HD") as hidden:
        assert hidden.handle.id > 0
        assert not hidden.is_closed

    assert hidden.is_closed

    with Mod.create("DT") as dt:
        dt.set_setting_bool("test", True)


def test_mods_collection():
    with ModsCollection.create() as mods:
        assert mods.handle.id > 0

        dt = Mod.create("DT")
        hd = Mod.create("HD")

        mods.add(dt)
        mods.add(hd)

        assert mods.has(dt)
        assert mods.has(hd)

        mods.remove(hd)
        assert not mods.has(hd)
        assert mods.has(dt)

        mods.debug()

    assert dt.is_closed


def test_beatmap_error_handling():
    try:
        Beatmap.from_file("nonexistent.osu")
        assert False, "Expected an error when loading a nonexistent beatmap"
    except RuntimeError as e:
        assert "Failed to create beatmap" in str(e)
