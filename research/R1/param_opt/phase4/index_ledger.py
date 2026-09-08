"""Add a narrow covering index to this unit's own ledger; no objective calls."""
import sqlite3,json,time
from pathlib import Path
out=Path('formal');db=sqlite3.connect(out/'state.sqlite',timeout=10)
before=list(db.execute('EXPLAIN QUERY PLAN SELECT count(*) FROM calls'))
started=time.time()
db.execute('CREATE INDEX IF NOT EXISTS calls_status_idx ON calls(status)');db.commit()
after=list(db.execute('EXPLAIN QUERY PLAN SELECT count(*) FROM calls'))
report=dict(start_epoch=started,wall_seconds=time.time()-started,before=before,after=after,
  note='Only a covering index was added. No row, objective, source code, deadline, or cap changed.')
(out/'ledger_index.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));db.close()
