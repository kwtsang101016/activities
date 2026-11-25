# Appendix A · Google Sheets visit log (demo kit)

Anonymous usage logging for the Vibe Coding workshop slides.

## What students see

Front-end page → `POST` JSON → Google Apps Script `doPost` → new row in `usage_log`.

## Fields (anonymous only)

| Column | Meaning |
|--------|---------|
| `timestamp` | ISO time from the browser |
| `sessionId` | Random id for this browser tab |
| `page` | Page / scene title |
| `project` | Short project label |
| `userAgent` | Optional browser string (no name/SID) |

Do **not** log student names, SIDs, emails, or typed personal answers.

## Live demo endpoint

Web app URL (instructor demo):

```text
https://script.google.com/macros/s/AKfycbw0Pp_vfh7AMpHjEXKh8FAzzXx-ALxrA4AyXcZvlFU2X5RDKrQhG0anh72p9YFC_v50sw/exec
```

Sheet: [Vibe Coding usage log](https://docs.google.com/spreadsheets/d/15n_xQsVvaeaEdKbx7IkWr8wQ7gIz-NyNbZ1p7k6OKJE/edit)

If POSTs return 401, open **Deploy → Manage deployments**, edit the web app, set **Who has access: Anyone**, then **New version** / redeploy. Open the `/exec` URL once in a browser while signed in if Google asks to authorize the script.

## Instructor setup (about 5 minutes)

1. Open [Google Sheets](https://sheets.google.com) → **Blank spreadsheet**.
2. Name it e.g. `Vibe Coding usage log`.
3. Rename Sheet1 to `usage_log`.
4. Row 1 headers:

   `timestamp` | `sessionId` | `page` | `project` | `userAgent`

5. **Extensions → Apps Script**.
6. Delete the stub code; paste everything from `Code.gs` → **Save**.
7. Optional: run `setupUsageLogSheet` once (Run ▶) to create/fix headers.
8. **Deploy → New deployment**:
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
9. Authorize Google if prompted → copy the `/exec` URL.
10. Open `demo.html` in a browser (or host it later), paste the URL, click **Send test visit**.
11. Refresh the Sheet — a new row should appear.

## Student / IDE prompt (from slides)

```text
Add anonymous visit logging to this static HTML app.
Post only timestamp, random sessionId, and page title to a Google Apps Script URL placeholder.
Do not collect names or personal data. Fail silently if the network request fails.
```

## CORS tip

Use:

```js
headers: { "Content-Type": "text/plain;charset=utf-8" }
```

so the browser does not send a CORS preflight that Apps Script often blocks.
