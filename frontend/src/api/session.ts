import { api } from "./axios";

export interface ChatSession {
  id: number;
  workspace_id: number;

  title: string;

  provider: string;
  model: string;

  created_at: string;
  updated_at: string;
}

export interface CreateChatSessionRequest {
  workspace_id: number;

  title?: string;

  provider?: string;
  model?: string;
}

export async function getChatSessions(): Promise<ChatSession[]> {
  const response = await api.get("/chat-sessions/");
  return response.data;
}

export async function createChatSession(
  payload: CreateChatSessionRequest
): Promise<ChatSession> {
  const response = await api.post(
    "/chat-sessions/",
    payload
  );

  return response.data;
}

export async function deleteChatSession(
  id: number
): Promise<void> {
  await api.delete(
    `/chat-sessions/${id}`
  );
}