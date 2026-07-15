// A thin typed wrapper over the orchestrator REST API.
const BASE = process.env.ORCHESTRATOR_URL ?? "http://localhost:8000";

async function http<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${method} ${path} -> ${res.status}: ${detail}`);
  }
  return (res.status === 204 ? undefined : await res.json()) as T;
}

export interface Run {
  id: string;
  task_id: string;
  status: "QUEUED" | "RUNNING" | "SUCCEEDED" | "FAILED";
  iterations: number;
}

export interface RunEvent {
  id: string;
  node: string;
  status: string;
  started_at: string;
  error: string | null;
}

export const api = {
  createProject: (name: string, repo_path: string) =>
    http<{ id: string }>("POST", "/projects", { name, repo_path }),
  createTask: (projectId: string, description: string) =>
    http<{ id: string }>("POST", `/projects/${projectId}/tasks`, { description }),
  startRun: (taskId: string) => http<Run>("POST", `/tasks/${taskId}/runs`),
  getRun: (runId: string) => http<Run>("GET", `/runs/${runId}`),
  getEvents: (runId: string) =>
    http<{ events: RunEvent[] }>("GET", `/runs/${runId}/events`),
};
