"""
Script to build all wheels.

Can be run from any Unix machine.
Relies on the build hook in `hatch_build.py` consuming OSU_NATIVE_WHEEL_TAG.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import zipfile
from subprocess import run

# Define platform tags. These are pairs of platform-name and wheel-tag. The
# former is used to locate the native binary, the latter is used to give the
# resulting wheel the correct name. Note that the build system does
# not check the name, so a typo here results in a broken wheel.

PLATFORM_TAGS = [
    ("win-x64", "win_amd64"),
    ("osx-arm64", "macosx_11_0_arm64"),
    ("linux-x64", "manylinux_2_38_x86_64"),
    ("linux-arm64", "manylinux_2_38_aarch64"),
    ("linux-arm", "manylinux_2_38_armv7l"),
]

if not sys.platform.startswith(("darwin", "win")):
    print("WARNING: Building releases only really works on Unix")

# Make sure we're in the project root, no matter where this is called from.
root_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
os.chdir(root_dir)
print(os.getcwd())

# Remove the dist directory for a fresh start
if os.path.isdir("dist"):
    shutil.rmtree("dist")

# Find the platforms whose native binary is present locally
bin_root = os.path.join("src", "osu_native_py", "native", "bin")
tag_for = dict(PLATFORM_TAGS)
present = []
for platform_name in tag_for:
    platform_dir = os.path.join(bin_root, platform_name)
    if os.path.isdir(platform_dir):
        lib_files = os.listdir(platform_dir)
        if len(lib_files) == 1:
            present.append(platform_name)

if not present:
    raise SystemExit("No native binaries found. Run 'make all' first.")

# Build a wheel for each present platform
for platform_name in present:
    wheel_tag = tag_for[platform_name]
    os.environ["OSU_NATIVE_WHEEL_TAG"] = wheel_tag
    print(f"Building wheel for {platform_name} -> {wheel_tag}")
    run([sys.executable, "-m", "build", "-n", "-w"])

# Build sdist
run([sys.executable, "-m", "build", "-n", "-s"])

# Checks produced files
all_tags = {tag_for[p] for p in present}
assert len(all_tags) == len(present), "Wheel tags in PLATFORM_TAGS are not unique"

found_files = os.listdir("dist")
found_wheels = [fname for fname in found_files if fname.endswith(".whl")]
found_tags = {fname.split("none-")[1].split(".")[0] for fname in found_wheels}
assert found_tags == all_tags, f"Found tags does not match expected tags: {found_tags}\n{all_tags}"

found_others = list(set(found_files) - set(found_wheels))
assert len(found_others) == 1 and found_others[0].endswith(
    ".tar.gz",
), f"Found unexpected files: {found_others}"

for archive_name in found_wheels:
    assert "-any-" not in archive_name, f"There should not be an 'any' wheel: {archive_name}"

# Report and check content of archives
print("Dist archives:")

# Simple check for sdist archive
for archive_name in found_others:
    size = os.stat("dist/" + archive_name).st_size
    print(f"{archive_name}  ({size / 1e6:0.2f} MB)")
    assert size < 1e6, f"Did not expected {archive_name} to be this large"

# Collect content of each wheel
hash_to_file: dict[str, str] = {}
for archive_name in found_wheels:
    size = os.stat("dist/" + archive_name).st_size
    print(f"{archive_name}  ({size / 1e6:0.2f} MB)")
    z = zipfile.ZipFile("dist/" + archive_name)
    flat_map = {os.path.basename(fi.filename): fi.filename for fi in z.filelist}
    lib_hashes = []
    for fname in flat_map:
        if fname.endswith((".so", ".dll", ".dylib")):
            bb = z.read(flat_map[fname])
            hash = hashlib.sha256(bb).hexdigest()
            lib_hashes.append(hash)
            print(f"    - {fname}  ({len(bb) / 1e6:0.2f} MB)\n      {hash}")
    assert (
        len(lib_hashes) == 1
    ), f"Expected 1 lib per wheel, got {len(lib_hashes)} in {archive_name}"
    hash = lib_hashes[0]
    assert hash not in hash_to_file, f"Same lib found in {hash_to_file[hash]} and archive_name"
    hash_to_file[hash] = archive_name

# Meta check
assert set(hash_to_file.values()) == set(found_wheels)
