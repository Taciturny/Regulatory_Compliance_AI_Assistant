"""Structural checks for the law and directive records used by the RAG index."""

from __future__ import annotations

import json
from pathlib import Path


def _load(path: Path) -> list[dict]:
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read legal source file: {path.name}") from exc
    if not isinstance(rows, list):
        raise ValueError(f"Legal source file must contain a list of records: {path.name}")
    return rows


def _check_sequence(rows: list[dict], key: str, expected: range, label: str) -> None:
    try:
        actual = [int(row["Id"]) for row in rows]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{label} records need numeric Id values.") from exc
    if sorted(actual) != list(expected) or len(actual) != len(set(actual)):
        raise ValueError(f"{label} coverage is incomplete or duplicated: expected IDs {expected.start}-{expected.stop - 1}.")
    if any(not str(row.get(key, "")).strip() or not str(row.get("Content", "")).strip() for row in rows):
        raise ValueError(f"Every {label} record must include its heading and full text.")


def validate_legal_corpus(documents_dir: Path) -> dict[str, int]:
    """Fail indexing unless all numbered provisions/schedules and DPO material exist."""
    ndpa = _load(documents_dir / "ndpa.json")
    gaid = _load(documents_dir / "gaid.json")
    schedules = _load(documents_dir / "gaid_schedules.json")
    programme = _load(documents_dir / "ndpc_dpo_pathway.json")
    _check_sequence(ndpa, "Section", range(1, 66), "NDPA section")
    _check_sequence(gaid, "Article", range(1, 53), "GAID article")
    _check_sequence(schedules, "Schedule", range(1, 11), "GAID schedule")
    _check_sequence(programme, "Program", range(1, 2), "NDPC DPO programme guidance")

    section_26 = next(row for row in ndpa if int(row["Id"]) == 26)
    section_32 = next(row for row in ndpa if int(row["Id"]) == 32)
    article_14 = next(row for row in gaid if int(row["Id"]) == 14)
    schedule_3 = next(row for row in schedules if int(row["Id"]) == 3)
    if "consent" not in section_26["Section"].lower():
        raise ValueError("NDPA section 26 must be the consent provision.")
    if not all(term in section_32["Content"].lower() for term in ("expert knowledge", "data protection law", "data protection officer")):
        raise ValueError("NDPA section 32 is missing its DPO competence standard.")
    if not all(term in article_14["Content"].lower() for term in ("credential assessment", "certification")):
        raise ValueError("GAID Article 14 is missing its DPO credential requirements.")
    if not all(term in schedule_3["Content"].lower() for term in ("examination", "continuous professional development")):
        raise ValueError("GAID Schedule 3 is missing DPO assessment metrics.")
    if "not an additional qualification prescribed" not in programme[0]["Content"].lower():
        raise ValueError("NDPC programme information must be clearly distinguished from legal requirements.")
    return {"ndpa_sections": len(ndpa), "gaid_articles": len(gaid), "gaid_schedules": len(schedules), "ndpc_programme_guides": len(programme)}
