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

## Open / Close session (Render free hours)

The classroom starts **closed** after every cold start. Students cannot use seating until you open a session.

1. Tap **Join classroom**
2. Tap **Instructor PIN** and enter `INSTRUCTOR_PIN`
3. Tap **Open session** — participants can then Join and sit
4. After class, tap **Close session** (disconnects everyone)

If no instructor stays connected for **3 hours** while the session is open, the server **auto-closes** the session. Prefer **Suspend** `consult2027-cat` on Render when you are not running a workshop. Do not leave CAT tabs open afterward (Socket.IO keeps the free instance awake).

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

### Live poll (A–D)

While the session is open, the instructor can start an anonymous multiple-choice poll. Anyone connected may vote; live bars are visible to everyone. Lock voting to discuss, then clear for the next question. Auto-close after **3 hours** with no instructor is only a safety net — tap **Close session** after class. Prefer **Suspend** `consult2027-cat` on Render between teaching weeks.

