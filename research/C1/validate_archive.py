"""Local structural and archive checks only, not a mathematical verifier."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    files = sorted(p for p in root.rglob('*') if p.is_file())
    required = ['RESULT.md','frozen_statement.md','proof.md','attempts.md','sources.md','verification.md','HANDOFF.md','MANIFEST.sha256','checkpoint.json','README.md','requirements.txt','reproduce.py']
    missing = [x for x in required if not (root/x).is_file()]
    assert not missing, missing
    bindings = {'geometry/proof.md':'7c7082a59d695ef87c9549337f8722d98513d401aa872a9e86eaca3df766717e','geometry/sparse_proof.md':'b096a9986d123652849704ed001439b63373591153f4bbd321f8023d9ab98e9f'}
    for rel, expected in bindings.items():
        assert hashlib.sha256((root/rel).read_bytes()).hexdigest() == expected, rel
    assert (root/'proof.md').read_bytes() == (root/'proofs/integrated_proof.md').read_bytes()
    syntax = []
    for path in files:
        if path.suffix == '.py':
            compile(path.read_text(encoding='utf-8-sig'), str(path.relative_to(root)), 'exec')
            syntax.append(path.relative_to(root).as_posix())
        if path.suffix == '.json':
            json.loads(path.read_text(encoding='utf-8-sig'))
    listed = {}
    for line in (root/'MANIFEST.sha256').read_text(encoding='utf-8-sig').splitlines():
        checksum, rel = line.split('  ', 1)
        assert rel not in listed, rel
        assert hashlib.sha256((root/rel).read_bytes()).hexdigest() == checksum.lower(), rel
        listed[rel] = checksum
    expected = {p.relative_to(root).as_posix() for p in files if p != root/'MANIFEST.sha256'}
    assert set(listed) == expected, (set(listed)-expected, expected-set(listed))
    zip_count = None
    if args.zip:
        with zipfile.ZipFile(args.zip) as archive:
            entries = [i for i in archive.infolist() if not i.is_dir()]
            zip_count = len(entries)
            assert len({i.filename for i in entries}) == len(entries)
            assert {i.filename for i in entries} == expected | {'MANIFEST.sha256'}
            for item in entries:
                assert archive.read(item) == (root/item.filename).read_bytes(), item.filename
    result = {'status':'PASS','scope':'structure, syntax, JSON, frozen-byte bindings, manifest and optional ZIP only','file_count':len(files),'python_syntax_files':syntax,'manifest_entries':len(listed),'zip_entries_verified':zip_count,'mathematical_verification':False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
