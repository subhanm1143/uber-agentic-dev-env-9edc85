import { api, RunEvent } from "../apiClient";

const TERMINAL = new Set(["SUCCEEDED", "FAILED"]);

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

// Start a run and stream new events until it reaches a terminal state.
export async function watchRun(taskId: string): Promise<number> {
  const run = await api.startRun(taskId);
  console.log(`run started: ${run.id}`);

  const seen = new Set<string>();
  for (;;) {
    const [{ events }, current] = await Promise.all([
      api.getEvents(run.id),
      api.getRun(run.id),
    ]);
    for (const ev of events as RunEvent[]) {
      if (!seen.has(ev.id)) {
        seen.add(ev.id);
        const mark = ev.error ? "✗" : "•";
        console.log(`  ${mark} ${ev.node} ${ev.status}${ev.error ? ` (${ev.error})` : ""}`);
      }
    }
    if (TERMINAL.has(current.status)) {
      console.log(`run ${current.status.toLowerCase()} after ${current.iterations} iteration(s)`);
      return current.status === "SUCCEEDED" ? 0 : 1;
    }
    await sleep(1000);
  }
}
