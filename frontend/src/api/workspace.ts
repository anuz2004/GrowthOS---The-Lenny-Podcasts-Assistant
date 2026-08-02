import { api } from "./axios";

export interface Workspace {
  id: number;
  title: string;
  description: string;
  icon: string;
  color: string;
  default_model: string;
  mode: string;
}

export async function getWorkspaces(): Promise<Workspace[]> {
  const response = await api.get("/workspaces");
  return response.data;
}

export async function createWorkspace(data: {
  title: string;
  description: string;
  icon: string;
  color: string;
  default_model: string;
  mode: string;
}) {
  const response = await api.post(
    "/workspaces",
    data
  );

  return response.data;
}

export async function deleteWorkspace(
  id: number
): Promise<void> {
  await api.delete(
    `/workspaces/${id}`
  );
}