# Activities

Public pages for School of Data Science activities.

- Statistics consultation landing: [`consult2027/`](https://kwtsang101016.github.io/activities/consult2027/)
- Consultation calendar: [`consult2027/calendar/`](https://kwtsang101016.github.io/activities/consult2027/calendar/)
- Consultant Attending Table (CAT): source in `cat/`, live at https://consult2027-cat.onrender.com/

## Develop

```bash
# Calendar (static, GitHub Pages)
cd calendar && npm install && npm run build

# CAT (Render / local Node)
cd cat && npm install && npm run dev
```

Regenerate CAT roster from the interest survey:

```bash
python scripts/build_consult_roster.py
```

Import a saved CAT attendance CSV into the calendar:

```bash
python scripts/import_attendance_csv.py cat/data/Consult2027-CAT-attendance-YYYYMMDD-HHMM.csv --date YYYY-MM-DD --label "CAT · Session title"
# then set attendanceFile on that date in calendar/src/data/schedule.ts and:
cd calendar && npm run build
```
