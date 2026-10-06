from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from ctypesgen.options import get_default_options
from ctypesgen.parser import parse
from ctypesgen.printer_python import WrapperPrinter
from ctypesgen.processor import process
from generate_models import generate_models

C_TYPES = """\
typedef unsigned char uint8_t;
typedef unsigned int uint32_t;
typedef int int32_t;
typedef long long int64_t;
"""


class FailOnError(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        raise RuntimeError(f"Binding generation failed: {record.getMessage()}")


def normalize_header(text: str) -> str:
    match = re.search(
        r"typedef struct ManagedObjectHandle\s*\{.*?\}\s*ManagedObjectHandle;",
        text,
        re.DOTALL,
    )
    if match is None or "typedef struct NativeBeatmap" not in text:
        raise RuntimeError("Missing native handle or beatmap declaration")

    handle = match.group(0)
    text = text.replace(handle, "").replace(
        "typedef struct NativeBeatmap",
        f"{handle}\n\ntypedef struct NativeBeatmap",
        1,
    )
    return text.replace("#include <stdint.h>", C_TYPES).replace(
        "#include <stdbool.h>",
        "#define bool _Bool",
    )


def generate(publish: Path, output: Path) -> None:
    work = publish / "python-bindings"
    work.mkdir(parents=True, exist_ok=True)
    header = work / "cabinet.h"
    temporary = work / "bindings.py"
    header.write_text(
        normalize_header((publish / "cabinet.h").read_text(encoding="utf-8-sig")),
        encoding="utf-8",
    )

    options = get_default_options()
    options.headers = [str(header)]
    options.libraries = ["osu.Native"]
    options.compile_libdirs = [str(publish)]
    options.cpp = "gcc -std=c11 -E -undef"
    options.include_macros = False
    options.show_macro_warnings = False
    options.no_gnu_types = True

    logger = logging.getLogger("ctypesgen")
    handler = FailOnError(logging.ERROR)
    logger.addHandler(handler)
    try:
        descriptions = parse(options.headers, options)
        process(descriptions, options)
        models = generate_models(descriptions)
        WrapperPrinter(str(temporary), options, descriptions)
    finally:
        logger.removeHandler(handler)

    contents = temporary.read_text(encoding="utf-8")
    loader = "add_library_search_dirs([])"
    if contents.count(loader) != 1:
        raise RuntimeError("Unexpected ctypesgen loader output")
    contents = contents.replace(
        loader,
        "from . import BIN_DIR\nadd_library_search_dirs([str(BIN_DIR)])",
    )
    compile(contents, str(output), "exec")
    for name, source in models.items():
        compile(source, str(output.with_name(name)), "exec")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(contents, encoding="utf-8")
    for name, source in models.items():
        output.with_name(name).write_text(source, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "src/osu_native_py/native/bindings.py",
    )
    args = parser.parse_args()
    generate(args.publish.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
