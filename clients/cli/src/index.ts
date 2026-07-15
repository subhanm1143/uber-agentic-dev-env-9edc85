#!/usr/bin/env node
import { createProject } from "./commands/project";
import { submitTask } from "./commands/task";
import { watchRun } from "./commands/run";

async function main(): Promise<void> {
  const [cmd, ...args] = process.argv.slice(2);
  switch (cmd) {
    case "project":
      await createProject(args[0], args[1]);
      break;
    case "task":
      await submitTask(args[0], args[1]);
      break;
    case "run":
      process.exitCode = await watchRun(args[0]);
      break;
    default:
      console.error("usage: agentctl <project|task|run> ...");
      process.exitCode = 2;
  }
}

main().catch((err) => {
  console.error(err.message);
  process.exitCode = 1;
});
