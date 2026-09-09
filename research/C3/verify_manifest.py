"""Verify a extracted C3 result bundle; no network or optional dependency."""
import hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
count=0
for line in (root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
    expected,relative=line.split('  ',1)
    target=(root/relative).resolve()
    if not target.is_relative_to(root):raise SystemExit('invalid manifest path')
    actual=hashlib.sha256(target.read_bytes()).hexdigest()
    if actual!=expected:raise SystemExit('HASH_MISMATCH: '+relative)
    count+=1
print('VERIFIED',count,'files')
