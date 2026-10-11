"""Create or refresh CivicData's Pinecone legal-source index."""

from pathlib import Path
import argparse

from dotenv import load_dotenv

from app.legal_corpus import validate_legal_corpus
from app.vector_store import LegalVectorStore


ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    load_dotenv(ROOT / ".env")
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--rebuild", action="store_true", help="Replace vectors in the current index namespace.")
    actions.add_argument("--reset-index", action="store_true", help="DELETE the entire configured Pinecone index, recreate it, and index the full corpus.")
    args = parser.parse_args()
    coverage = validate_legal_corpus(ROOT / "documents")
    print("Validated complete corpus:", ", ".join(f"{count} {name.replace('_', ' ')}" for name, count in coverage.items()))
    store = LegalVectorStore(ROOT / "documents")
    if args.reset_index:
        print(f"Deleting and recreating Pinecone index '{store.index_name}' using the configured cloud and region.")
        store.reset_index()
    indexed = store.build(force=args.rebuild or args.reset_index)
    print(f"Indexed {indexed} legal passages in Pinecone index '{store.index_name}'.")


if __name__ == "__main__":
    main()
