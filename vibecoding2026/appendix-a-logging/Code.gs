/**
 * Anonymous visit logger for the Vibe Coding workshop (Appendix A).
 *
 * Sheet setup:
 * 1. Create a Google Sheet named e.g. "Vibe Coding usage log".
 * 2. Rename the first tab to: usage_log
 * 3. Put headers in row 1:
 *    timestamp | sessionId | page | project | userAgent
 * 4. Extensions → Apps Script → paste this file → Save
 * 5. Deploy → New deployment → Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 6. Copy the web app URL into demo.html (LOG_URL).
 */

var SHEET_NAME = "usage_log";
var HEADERS = ["timestamp", "sessionId", "page", "project", "userAgent"];

function ensureSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function doGet() {
  return ContentService.createTextOutput(
    JSON.stringify({
      ok: true,
      message: "POST JSON { timestamp, sessionId, page, project } to log a visit.",
    }),
  ).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var raw = (e && e.postData && e.postData.contents) || "{}";
    var data = JSON.parse(raw);
    var sheet = ensureSheet_();

    var timestamp =
      typeof data.timestamp === "string" && data.timestamp
        ? data.timestamp
        : new Date().toISOString();
    var sessionId =
      typeof data.sessionId === "string" ? String(data.sessionId).slice(0, 64) : "";
    var page = typeof data.page === "string" ? String(data.page).slice(0, 120) : "";
    var project =
      typeof data.project === "string" ? String(data.project).slice(0, 80) : "vibe-coding";
    var userAgent =
      typeof data.userAgent === "string" ? String(data.userAgent).slice(0, 180) : "";

    // Never trust / store free-form PII fields even if a client sends them.
    sheet.appendRow([timestamp, sessionId, page, project, userAgent]);

    return ContentService.createTextOutput(
      JSON.stringify({ ok: true }),
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ ok: false, error: String(err) }),
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

/** Optional: run once from the editor to create the usage_log tab + headers. */
function setupUsageLogSheet() {
  ensureSheet_();
}
