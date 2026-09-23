/** Consultation / vibe-coding schedule from Tentative Plan.txt */

export type EventKind = "workshop" | "consultation" | "info" | "faq";

export interface CourseEvent {
  /** ISO date YYYY-MM-DD */
  date: string;
  title: string;
  kind: EventKind;
  /** Highlight in red for workshops / FAQ sessions if desired */
  special?: boolean;
  /** Optional attendance snapshot under public/attendance/{date}.json */
  attendanceFile?: string;
}

export const COURSE_EVENTS: CourseEvent[] = [
  { date: "2026-09-23", title: "Info session + Vibe coding workshop", kind: "info" },
  { date: "2026-10-14", title: "Vibe coding workshop", kind: "workshop" },
  { date: "2026-11-04", title: "Vibe coding workshop", kind: "workshop" },
  { date: "2026-11-18", title: "Vibe coding workshop", kind: "workshop" },
  { date: "2027-02-19", title: "Consultation", kind: "consultation" },
  { date: "2027-03-05", title: "Consultation", kind: "consultation" },
  { date: "2027-03-19", title: "Consultation", kind: "consultation" },
  { date: "2027-03-26", title: "FAQ Workshop 1", kind: "faq", special: true },
  { date: "2027-04-02", title: "Consultation", kind: "consultation" },
  { date: "2027-04-16", title: "Consultation", kind: "consultation" },
  { date: "2027-04-30", title: "Consultation", kind: "consultation" },
  { date: "2027-05-07", title: "FAQ Workshop 2", kind: "faq", special: true },
];

export function eventsByDate(events: CourseEvent[]): Map<string, CourseEvent[]> {
  const map = new Map<string, CourseEvent[]>();
  for (const event of events) {
    const list = map.get(event.date) ?? [];
    list.push(event);
    map.set(event.date, list);
  }
  return map;
}

export function isSpecialEvent(event: CourseEvent): boolean {
  return Boolean(event.special) || event.kind === "faq";
}
