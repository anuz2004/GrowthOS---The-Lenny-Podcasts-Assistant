import {api} from "./axios";

export interface Message {
  id: number;
  chat_session_id?: number;
  role: string;
  content: string;
  created_at: string;
}

export async function getMessages(sessionId: number): Promise<Message[]> {
  const response = await api.get(`/messages/${sessionId}`);
  return response.data;
}