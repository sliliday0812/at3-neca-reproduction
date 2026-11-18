"""Verify every vendored upstream file against the frozen source manifest."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'docs/upstream-files-sha256.json').read_text())
for name,digest in expected.items():
 file=root/'vendor/NeCA'/name
 if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:raise SystemExit('UPSTREAM_MISMATCH '+name)
print('UPSTREAM_INTEGRITY_PASS',len(expected),'files')
