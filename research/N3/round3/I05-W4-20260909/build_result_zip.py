#!/usr/bin/env python3
"""Restore the exact submitted I05-W4 result ZIP from tracked Base64 chunks."""
from __future__ import annotations

import argparse
import base64
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD_DIR = HERE / "payload"
EXPECTED_SHA256 = "b408d1e8faa8bd99e2df33e03dc00548ff42c4e22ef3e814838049820000c308"
EXPECTED_SIZE = 42902
DEFAULT_OUTPUT = HERE / "I05-W4-20260909_result.zip"


def restore(output: Path) -> tuple[int, str]:
    parts = sorted(PAYLOAD_DIR.glob("I05-W4-20260909_result.zip.b64.*"))
    if not parts:
        raise SystemExit(f"no payload chunks found under {PAYLOAD_DIR}")
    encoded = "".join("".join(path.read_text(encoding="ascii").split()) for path in parts)
    data = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        raise SystemExit(
            "payload verification failed: "
            f"size={len(data)} sha256={digest}; "
            f"expected size={EXPECTED_SIZE} sha256={EXPECTED_SHA256}"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return len(data), digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    size, digest = restore(args.output)
    print(f"restored {args.output}")
    print(f"bytes={size}")
    print(f"sha256={digest}")


if __name__ == "__main__":
    main()
