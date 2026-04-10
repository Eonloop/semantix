from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app.eval.metrics import mean, recall_at_k, reciprocal_rank
from app.eval.qrels import load_qrels_markdown
from app.ingest import Ingestor
from app.query import Query

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def main() -> int:
    parser = argparse.ArgumentParser(description="Mean MRR and Recall@K on eval_corpus qrels.")
    parser.add_argument(
        "--eval-dir",
        type=Path,
        default=_REPO_ROOT / "eval_corpus",
        help="Directory containing doc-*.md and eval_queries_and_qrels.md",
    )
    parser.add_argument(
        "--qrels",
        type=Path,
        default=None,
        help="Path to eval_queries_and_qrels.md (default: <eval-dir>/eval_queries_and_qrels.md)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="sentence-transformers model id",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="Chroma persistence directory (default: temporary, removed after run)",
    )
    parser.add_argument(
        "--skip-ingest",
        action="store_true",
        help="Use existing --db without re-ingesting (must already contain policies collection)",
    )
    parser.add_argument(
        "--max-rank",
        type=int,
        default=10,
        help="Retrieve up to this many chunks per query for scoring",
    )
    parser.add_argument(
        "--k",
        type=int,
        nargs="+",
        default=[1, 3, 5],
        help="Recall@K values to report",
    )
    args = parser.parse_args()

    eval_dir: Path = args.eval_dir
    qrels_path = args.qrels or (eval_dir / "eval_queries_and_qrels.md")
    if not qrels_path.is_file():
        print(f"Missing qrels file: {qrels_path}", file=sys.stderr)
        return 1

    pairs = load_qrels_markdown(qrels_path)
    if not pairs:
        print(f"No query/qrel pairs parsed from {qrels_path}", file=sys.stderr)
        return 1

    cleanup_db = False
    if args.db is not None:
        db_path = str(args.db.resolve())
    else:
        tmp = tempfile.mkdtemp(prefix="semantix-eval-")
        db_path = tmp
        cleanup_db = True

    if not args.skip_ingest:
        ingestor = Ingestor(vector_db_path=db_path, model_name=args.model)
        doc_files = sorted(eval_dir.glob("doc-*.md"))
        if not doc_files:
            print(f"No doc-*.md under {eval_dir}", file=sys.stderr)
            return 1
        for p in doc_files:
            ingestor.ingest(str(p))
    else:
        if args.db is None:
            print("--skip-ingest requires --db", file=sys.stderr)
            return 1

    engine = Query(model_name=args.model, vector_db_path=db_path)
    max_k = max(max(args.k), args.max_rank)

    mrr_scores: list[float] = []
    recall_scores: dict[int, list[float]] = {k: [] for k in args.k}

    print(f"Queries: {len(pairs)} | model: {args.model} | db: {db_path}")
    print(f"Retrieving top {max_k} chunks per query\n")

    for query_text, frags in pairs:
        documents, metadatas = engine.query(query_text, k=max_k)
        if not metadatas:
            mrr_scores.append(0.0)
            for k in args.k:
                recall_scores[k].append(0.0)
            continue
        mrr_scores.append(reciprocal_rank(metadatas, frags))
        for k in args.k:
            recall_scores[k].append(recall_at_k(metadatas, frags, k))

    print(f"Mean MRR:        {mean(mrr_scores):.4f}")
    for k in sorted(args.k):
        print(f"Mean Recall@{k}:   {mean(recall_scores[k]):.4f}")

    if cleanup_db:
        import shutil

        shutil.rmtree(db_path, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
