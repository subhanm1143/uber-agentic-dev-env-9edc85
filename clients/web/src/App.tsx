import { useEffect, useRef, useState } from "react";
import { api, Run, RunEvent } from "./api/client";
import { ProjectPicker } from "./components/ProjectPicker";
import { TaskComposer } from "./components/TaskComposer";
import { RunTimeline } from "./components/RunTimeline";

const TERMINAL = new Set(["SUCCEEDED", "FAILED"]);
const PROJECTS = [{ id: "demo", name: "Demo project" }];

export default function App() {
  const [projectId, setProjectId] = useState("");
  const [run, setRun] = useState<Run | null>(null);
  const [events, setEvents] = useState<RunEvent[]>([]);
  const timer = useRef<number | null>(null);

  async function start(description: string) {
    const task = await api.createTask(projectId, description);
    const started = await api.startRun(task.id);
    setRun(started);
    setEvents([]);
  }

  // Poll the active run until it reaches a terminal state.
  useEffect(() => {
    if (!run || TERMINAL.has(run.status)) return;
    timer.current = window.setInterval(async () => {
      const [{ events: evs }, current] = await Promise.all([
        api.getEvents(run.id),
        api.getRun(run.id),
      ]);
      setEvents(evs);
      setRun(current);
    }, 1000);
    return () => {
      if (timer.current) window.clearInterval(timer.current);
    };
  }, [run]);

  return (
    <main>
      <h1>Agentic Dev Environment</h1>
      <ProjectPicker projects={PROJECTS} value={projectId} onChange={setProjectId} />
      <TaskComposer disabled={!projectId} onSubmit={start} />
      {run && <RunTimeline status={run.status} events={events} />}
    </main>
  );
}
