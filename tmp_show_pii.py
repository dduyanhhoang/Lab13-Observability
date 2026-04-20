import json
from pathlib import Path
for line in Path('data/logs.jsonl').read_text().splitlines():
    r = json.loads(line)
    if 'REDACTED' in str(r.get('payload', {})):
        print(json.dumps(r, indent=2))
        break
