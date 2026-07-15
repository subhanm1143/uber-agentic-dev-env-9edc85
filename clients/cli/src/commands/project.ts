import { api } from "../apiClient";

export async function createProject(name: string, repoPath: string): Promise<void> {
  const project = await api.createProject(name, repoPath);
  console.log(`project created: ${project.id}`);
}
