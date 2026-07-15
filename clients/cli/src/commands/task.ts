import { api } from "../apiClient";

export async function submitTask(projectId: string, description: string): Promise<void> {
  const task = await api.createTask(projectId, description);
  console.log(`task created: ${task.id}`);
}
