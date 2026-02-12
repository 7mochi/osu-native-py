# osu-native-py

[![PyPI Version](https://img.shields.io/pypi/v/osu-native-py.svg)](https://pypi.org/project/osu-native-py/)
[![Python Version](https://img.shields.io/pypi/pyversions/osu-native-py.svg)](https://pypi.org/project/osu-native-py/)
[![License](https://img.shields.io/badge/license-mit%20license-brightgreen.svg)][license]

Python wrapper for [osu-native], providing difficulty and performance calculation for all [osu!] modes.

## Example

### Calculating performance

```python
from osu_native_py.wrapper.calculators import create_difficulty_calculator
from osu_native_py.wrapper.calculators import create_performance_calculator
from osu_native_py.wrapper.objects import Beatmap
from osu_native_py.wrapper.objects import Mod
from osu_native_py.wrapper.objects import ModsCollection
from osu_native_py.wrapper.objects import Ruleset
from osu_native_py.wrapper.objects import ScoreInfo

BEATMAP_PATH = "/path/to/file.osu"


beatmap = Beatmap.from_file(BEATMAP_PATH)
ruleset = Ruleset.from_id(0)
mods = ModsCollection.create()

for mod_name in ["DT", "CL"]:
    mod = Mod.create(mod_name)
    mods.add(mod)

score = ScoreInfo(
    accuracy=0.94,
    max_combo=116,
    count_great=65,
    count_meh=0,
    count_ok=6,
    count_miss=0,
)

diff_calc = create_difficulty_calculator(ruleset, beatmap)
diff_attrs = diff_calc.calculate(mods)

perf_calc = create_performance_calculator(ruleset)
perf_attrs = perf_calc.calculate(ruleset, beatmap, mods, score, diff_attrs)

print(perf_attrs.total)
```

## Installation

```bash
pip install osu-native-py
```

## Supported Platforms

- **Windows**: x64
- **Linux**: x64
- **macOS**: ARM64 (Apple Silicon)

## Thanks to
- [minisbett](https://github.com/minisbett) for maintaining [osu-native].
- [Lekuruu](https://github.com/Lekuruu) for helping me with Python-related questions and some cleanup of the code.

[osu!]: https://osu.ppy.sh/
[osu-native]: https://github.com/minisbett/osu-native
[license]: https://github.com/7mochi/osu-native-py/blob/master/LICENSE
