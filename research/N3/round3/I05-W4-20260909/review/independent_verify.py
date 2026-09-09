#!/usr/bin/env python3
"""Hash-check and execute the independently written verifier source payload."""
from __future__ import annotations

import base64
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD_DIR = HERE / "verifier_payload"
EXPECTED_SHA256 = "02cb42c069fcf8b78cd441c4dcc2880d1dd909f90bc1af4230df7570e484c3b2"
SYNTHETIC_SOURCE_PATH = HERE / "independent_verify.reconstructed.py"

parts = sorted(PAYLOAD_DIR.glob("independent_verify.py.b64.*"))
if not parts:
    raise SystemExit(f"no verifier payload chunks found under {PAYLOAD_DIR}")
encoded = "".join("".join(path.read_text(encoding="ascii").split()) for path in parts)
source = base64.b64decode(encoded, validate=True)
digest = hashlib.sha256(source).hexdigest()
if digest != EXPECTED_SHA256:
    raise SystemExit(
        f"verifier source hash mismatch: {digest}; expected {EXPECTED_SHA256}"
    )

namespace = {
    "__name__": "__main__",
    "__file__": str(SYNTHETIC_SOURCE_PATH),
    "__package__": None,
}
exec(compile(source, str(SYNTHETIC_SOURCE_PATH), "exec"), namespace)
