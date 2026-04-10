from __future__ import annotations

import re
from pathlib import Path


def load_qrels_markdown(path: Path) -> list[tuple[str, list[str]]]:

    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'Query:\s*"([^"]+)"\s*\n\s*- Relevant docs:\s*`([^`]+)`',
        re.MULTILINE,
    )
    out: list[tuple[str, list[str]]] = []
    for m in pattern.finditer(text):
        query = m.group(1).strip()
        doc = m.group(2).strip()
        out.append((query, [doc]))
    return out
