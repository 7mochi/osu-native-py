from __future__ import annotations

import os
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "build/generated/cabinet.h"

if not os.path.exists(filename):
    print(f"Error: {filename} not found. Please run the build script first to generate the header.")
    exit(1)

with open(filename) as f:
    lines = f.readlines()

handle_block = []
other_lines = []
inside_handle = False

for line in lines:
    if "typedef struct ManagedObjectHandle" in line:
        inside_handle = True
        handle_block.append(line)
        continue

    if inside_handle:
        handle_block.append(line)
        if "}" in line and ";" in line:
            inside_handle = False
        continue

    other_lines.append(line)

final_content = []
inserted = False

for line in other_lines:
    if "typedef struct NativeBeatmap" in line and not inserted:
        final_content.extend(handle_block)
        final_content.append("\n")
        inserted = True
    final_content.append(line)

with open(filename, "w") as f:
    f.writelines(final_content)

print(f"Cabinet header fix applied successfully.")
