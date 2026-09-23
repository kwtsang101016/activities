# Consult2027 Consultant Attending Table (CAT)

Realtime seating board for statistics consultation training sessions.

Name cards show **name, school, major, and year**. Students sit by tapping a card, then a seat, and confirming with their student ID.

## Links

- Project page: https://kwtsang101016.github.io/activities/consult2027/
- Vibe coding slides: https://kwtsang101016.github.io/vibe_coding_slides/
- Calendar: https://kwtsang101016.github.io/activities/consult2027/calendar/
- Live CAT (Render): https://consult2027-cat.onrender.com/

## Run locally

```bash
cd cat
npm install
npm run dev
```

Open http://localhost:3001 after `npm start` (or the Vite+server ports from `npm run dev`).

## Deploy on Render

1. Repo: [kwtsang101016/activities](https://github.com/kwtsang101016/activities) (or a dedicated CAT fork)
2. Blueprint uses root `render.yaml` with service name **`consult2027-cat`**
3. Set `INSTRUCTOR_PIN` in the Render dashboard
4. Optional Upstash Redis: `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`

## Roster

Regenerate from the interest survey workbook:

```bash
python scripts/build_consult_roster.py
```

- `cat/src/data/roster.json` — public fields (no raw student IDs)
- `cat/server/data/credentials.json` — SHA-256 hashes only
