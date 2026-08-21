"""
Hook for building wheels with the hatchling build backend.

- Set wheel to being platform-specific (not pure python).
- The native library is compiled beforehand and included in the wheel.
- Support cross-platform wheel building with a custom env var.
- Note that for sdist we go into pure-python mode.
"""

from __future__ import annotations

import os

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # See https://hatch.pypa.io/latest/plugins/builder/wheel/#build-data

        # We only tag wheels with a platform; sdist stays pure-python.
        if self.target_name == "wheel":
            build_data["pure_python"] = False

            wheel_tag = os.getenv("OSU_NATIVE_WHEEL_TAG")
            if wheel_tag:
                # A cross-platform build
                build_data["tag"] = "py3-none-" + wheel_tag
            else:
                # A build for this platform, e.g. ``pip install -e .``
                build_data["infer_tag"] = True
