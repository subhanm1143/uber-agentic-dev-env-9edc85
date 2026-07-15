import { RunEvent } from "../api/client";

interface Props {
  status: string;
  events: RunEvent[];
}

export function RunTimeline({ status, events }: Props) {
  return (
    <div className="timeline">
      <span className={`badge badge-${status.toLowerCase()}`}>{status}</span>
      <ol>
        {events.map((ev) => (
          <li key={ev.id} className={ev.error ? "event-error" : "event-ok"}>
            <strong>{ev.node}</strong> — {ev.status}
            {ev.error && <span className="error"> ({ev.error})</span>}
          </li>
        ))}
      </ol>
    </div>
  );
}
