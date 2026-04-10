from __future__ import annotations


def _meta_sources_contain(meta: dict | None, doc_fragment: str) -> bool:
    if not meta:
        return False
    src = meta.get("source") or ""
    return doc_fragment in src


def reciprocal_rank(metadatas: list[dict | None], relevant_fragments: list[str]) -> float:
    """Reciprocal rank of the first hit whose source contains any relevant fragment (1-based rank)."""
    if not relevant_fragments:
        return 0.0
    for i, meta in enumerate(metadatas):
        if any(_meta_sources_contain(meta, frag) for frag in relevant_fragments):
            return 1.0 / (i + 1)
    return 0.0


def recall_at_k(
    metadatas: list[dict | None],
    relevant_fragments: list[str],
    k: int,
) -> float:
    """Fraction of relevant fragments that appear in at least one of the top-k chunk metadatas."""
    if not relevant_fragments:
        return 0.0
    top = metadatas[:k]
    hits = 0
    for frag in relevant_fragments:
        if any(_meta_sources_contain(m, frag) for m in top):
            hits += 1
    return hits / len(relevant_fragments)


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
