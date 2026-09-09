#!/usr/bin/env python3
"""Build I05-W4-20260909_result.zip from the tracked submission tree."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "submission"
OUTPUT = HERE / "I05-W4-20260909_result.zip"
PREFIX = "I05-W4-20260909_result"

if not SOURCE.is_dir():
    raise SystemExit(f"missing source directory: {SOURCE}")

with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(p for p in SOURCE.rglob("*") if p.is_file()):
        archive.write(path, f"{PREFIX}/{path.relative_to(SOURCE).as_posix()}")

print(OUTPUT)
