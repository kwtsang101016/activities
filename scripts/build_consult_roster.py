# -*- coding: utf-8 -*-
"""Build consult2027 CAT roster.json + credentials.json from the interest survey."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import openpyxl

ROOT = Path(r"C:\Users\曾家炜\Desktop\工作\Work 2026\Name_card_workshop")
XLSX = ROOT / "09232026_Student Consultant Interest.xlsx"
CAT = ROOT / "activities-site" / "cat"

YEAR_MAP = {
    1: "Year 1",
    2: "Year 2",
    3: "Year 3",
    4: "Year 4",
    5: "Master's",
    6: "PhD",
}


def norm_school(raw: str) -> str:
    s = (raw or "").strip()
    key = s.lower().replace(" ", "")
    if key in {"sds", "数据科学学院"} or "data science" in s.lower():
        return "School of Data Science"
    if key in {"sai", "人工智能"} or "artificial" in s.lower() or s == "人工智能":
        return "School of Artificial Intelligence"
    return s or "—"


def norm_major(raw: str) -> str:
    s = (raw or "").strip()
    key = s.lower().replace(" ", "")
    mapping = {
        "ds": "Data Science",
        "datascience": "Data Science",
        "统计学": "Statistics",
        "statistics": "Statistics",
        "cse": "Computer Science and Engineering",
        "人工智能": "Artificial Intelligence",
    }
    return mapping.get(key, s or "—")


def norm_year(raw) -> str:
    try:
        return YEAR_MAP.get(int(raw), str(raw))
    except (TypeError, ValueError):
        return str(raw or "—")


def hash_sid(sid: str) -> str:
    normalized = re.sub(r"[^a-z0-9]", "", str(sid).strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).digest().hex()


def main() -> None:
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))[1:]

    people = [
        {
            "id": "instructor-tsang",
            "name": "曾家炜",
            "englishName": "Ka Wai Tsang",
            "role": "aa",
            "college": "School of Data Science",
            "major": "—",
            "year": "Instructor",
            "plan": "",
            "photo": "",
        }
    ]
    hashes: dict[str, str | None] = {"instructor-tsang": None}

    for row in rows:
        if not row or not row[6]:
            continue
        name = str(row[6]).strip()
        sid = str(row[7]).strip()
        school = norm_school(str(row[9] or ""))
        major = norm_major(str(row[10] or ""))
        year = norm_year(row[11])
        pid = f"stu-{sid}"
        people.append(
            {
                "id": pid,
                "name": name,
                "englishName": "",
                "role": "student",
                "college": school,
                "major": major,
                "year": year,
                "plan": f"{major} · {year}",
            }
        )
        hashes[pid] = hash_sid(sid)

    roster = {
        "course": "Consult2027",
        "section": "CAT",
        "classroom": "Consultation room",
        "people": people,
    }

    roster_path = CAT / "src" / "data" / "roster.json"
    cred_path = CAT / "server" / "data" / "credentials.json"
    roster_path.parent.mkdir(parents=True, exist_ok=True)
    cred_path.parent.mkdir(parents=True, exist_ok=True)
    roster_path.write_text(json.dumps(roster, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cred_path.write_text(
        json.dumps({"algo": "sha256-alnum-lower", "hashes": hashes}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(people)} people to {roster_path}")
    print(f"Wrote {len(hashes)} credential hashes to {cred_path}")


if __name__ == "__main__":
    main()
