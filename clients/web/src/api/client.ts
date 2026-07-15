const BASE = import.meta.env.VITE_ORCHESTRATOR_URL ?? "http://localhost:8000";

async function http<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`${method} ${path} -> ${res.status}`);
  return (await res.json()) as T;
}

export interface RunEvent {
  id: string;
  node: string;
  status: string;
  started_at: string;
  error: string | null;
}

export interface Run {
  id: string;
  status: "QUEUED" | "RUNNING" | "SUCCEEDED" | "FAILED";
  iterations: number;
}

export const api = {
  createTask: (projectId: string, description: string) =>
    http<{ id: string }>("POST", `/projects/${projectId}/tasks`, { description }),
  startRun: (taskId: string) => http<Run>("POST", `/tasks/${taskId}/runs`),
  getRun: (runId: string) => http<Run>("GET", `/runs/${runId}`),
  getEvents: (runId: string) =>
    http<{ events: RunEvent[] }>("GET", `/runs/${runId}/events`),
};
