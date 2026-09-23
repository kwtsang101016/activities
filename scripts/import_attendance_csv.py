# -*- coding: utf-8 -*-
"""Convert a CAT attendance CSV into calendar/public/attendance/YYYY-MM-DD.json."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER = ROOT / "cat" / "src" / "data" / "roster.json"
DEFAULT_OUT_DIR = ROOT / "calendar" / "public" / "attendance"
CAT_DIR = ROOT / "cat"
CAT_URL = "https://consult2027-cat.onrender.com"


def fetch_live_profiles() -> dict:
    script = textwrap.dedent(
        f"""
        import {{ io }} from 'socket.io-client';
        const url = {CAT_URL!r};
        const socket = io(url, {{ transports: ['websocket','polling'], timeout: 20000 }});
        const t = setTimeout(() => {{ console.error('timeout'); process.exit(1); }}, 25000);
        socket.on('snapshot', (snap) => {{
          clearTimeout(t);
          const out = {{ profiles: snap?.state?.profiles ?? {{}}, guests: snap?.state?.guests ?? [] }};
          process.stdout.write(JSON.stringify(out));
          socket.close();
          process.exit(0);
        }});
        socket.on('connect_error', (e) => {{ clearTimeout(t); console.error(String(e)); process.exit(1); }});
        """
    )
    try:
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=str(CAT_DIR),
            capture_output=True,
            text=True,
            timeout=35,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            dump = json.loads(result.stdout)
            profiles = dump.get("profiles") or {}
            print(f"Fetched {len(profiles)} live profiles from CAT")
            return profiles
        print("Live profile fetch skipped:", (result.stderr or result.stdout or "")[:240])
    except Exception as exc:  # noqa: BLE001
        print(f"Live profile fetch error: {exc}")
    return {}


def convert(csv_path: Path, date: str, label: str, roster_path: Path, out_dir: Path) -> Path:
    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    roster_by_id = {person["id"]: person for person in roster["people"]}
    profiles = fetch_live_profiles()

    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    if not rows:
        raise SystemExit(f"No rows in {csv_path}")

    people: list[dict] = []
    max_row = 0
    max_seat = 0
    present_n = 0

    for row in rows:
        present = row["present"] == "yes"
        placement = None
        if present and row.get("zone"):
            present_n += 1
            seat_idx = int(row["seat_index"])
            max_seat = max(max_seat, seat_idx)
            if row["zone"] == "student":
                row_n = int(row["row_label"].replace("Row ", "")) - 1
                max_row = max(max_row, row_n)
                placement = {"zone": "student", "row": row_n, "seat": seat_idx}
            else:
                placement = {"zone": "advisor", "row": 0, "seat": seat_idx}

        pid = row["person_id"]
        base = roster_by_id.get(pid, {})
        prof = profiles.get(pid, {}) if isinstance(profiles, dict) else {}
        role = row["role"] if row["role"] in {"aa", "pa", "student", "guest"} else base.get("role", "student")

        people.append(
            {
                "id": pid,
                "name": row["name"] or base.get("name", ""),
                "englishName": row.get("english_name") or base.get("englishName", "") or "",
                "role": role,
                "college": base.get("college", "") or "",
                "major": base.get("major", "") or "",
                "year": base.get("year", "") or "",
                "plan": base.get("plan", "") or "",
                "country": base.get("country", "") or "",
                "hobbies": base.get("hobbies", "") or "",
                "photo": base.get("photo", "") or "",
                "photoDataUrl": (prof.get("photoDataUrl") or "") if isinstance(prof, dict) else "",
                "nickname": (prof.get("nickname") or "") if isinstance(prof, dict) else "",
                "profileCollege": (prof.get("college") or "") if isinstance(prof, dict) else "",
                "profileCountry": (prof.get("country") or "") if isinstance(prof, dict) else "",
                "profileHobbies": (prof.get("hobbies") or "") if isinstance(prof, dict) else "",
                "present": present,
                "placement": placement,
            }
        )

    for person in people:
        if person["id"] == "instructor-tsang" and not person["photo"]:
            person["photo"] = "/photos/aa-tsang.png"

    snapshot = {
        "date": date,
        "course": rows[0]["course"],
        "section": rows[0]["section"],
        "recordedAt": rows[0]["recorded_at"],
        "label": label,
        "studentRowCount": max(max_row + 1, 4),
        "seatsPerRow": max(max_seat + 1, 8),
        "people": people,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date}.json"
    out_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"people={len(people)} present={present_n} layout={snapshot['studentRowCount']}x{snapshot['seatsPerRow']}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="CAT attendance CSV path")
    parser.add_argument("--date", required=True, help="Session date YYYY-MM-DD")
    parser.add_argument("--label", default="", help="Snapshot label shown in the calendar")
    parser.add_argument("--roster", type=Path, default=DEFAULT_ROSTER)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    label = args.label or f"CAT · {args.date}"
    convert(args.csv, args.date, label, args.roster, args.out_dir)


if __name__ == "__main__":
    main()
