import type { DisplayPerson } from "../lib/attendance";

interface NameCardProps {
  person: DisplayPerson;
  compact?: boolean;
  enlarged?: boolean;
}

export function NameCard({ person, compact = false, enlarged = false }: NameCardProps) {
  const roleLabel =
    person.role === "aa"
      ? "Instructor"
      : person.role === "pa"
        ? "PA"
        : person.role === "guest"
          ? "Guest"
          : "Consultant";

  const showTrueUnderNickname = person.displayName !== person.trueName;
  const school = person.displayCollege || "";
  const major = person.major || "";
  const year = person.year || "";

  if (compact && !enlarged) {
    return (
      <article className={["name-card", "name-card--compact", `name-card--${person.role}`].join(" ")}>
        <h3 className="name-card__name">{person.displayName}</h3>
        {showTrueUnderNickname ? <p className="name-card__true">{person.trueName}</p> : null}
      </article>
    );
  }

  return (
    <article
      className={[
        "name-card",
        `name-card--${person.role}`,
        enlarged ? "name-card--enlarged" : "",
        person.displayPhoto ? "name-card--has-photo" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      {person.displayPhoto ? (
        <img className="name-card__photo" src={person.displayPhoto} alt="" draggable={false} />
      ) : null}
      <div className="name-card__body">
        <span className="name-card__role">{roleLabel}</span>
        <h3 className="name-card__name">{person.displayName}</h3>
        {showTrueUnderNickname ? <p className="name-card__true">{person.trueName}</p> : null}
        {person.englishName ? <p className="name-card__english">{person.englishName}</p> : null}
        {school ? <p className="name-card__meta">{school}</p> : null}
        {major ? <p className="name-card__meta">{major}</p> : null}
        {year ? <p className="name-card__meta">{year}</p> : null}
      </div>
    </article>
  );
}
