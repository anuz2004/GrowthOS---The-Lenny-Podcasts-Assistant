import { api } from "./axios";
import type { GrowthOSError } from "../types/error";

export interface ChatMessage {
  id: number;
  role: string;
  content: string;
  created_at: string;
}

export interface Artifact {
  title: string;
  type: "markdown" | "html" | "text";
  content: string;
}

// export interface GrowthOSError {
//   title: string;
//   message: string;
//   suggestions: string[];
//   technical?: string;
//   status_code?: number;
// }

export interface ChatRequest {
  chat_session_id: number;
  message: string;
}

export interface ChatResponse {
  user: ChatMessage;
  assistant: ChatMessage;
  artifact?: Artifact | null;
  title?: string;
}

export async function sendChat(
  payload: ChatRequest
): Promise<ChatResponse> {
  try {
    const response = await api.post(
      "/chat/",
      payload
    );

    return response.data;
  } catch (err: any) {
    if (err.response?.data?.error) {
      throw err.response.data.error;
    }

    throw {
      title: "Request Failed",
      message:
        "Unable to communicate with the backend.",
      suggestions: [
        "Verify the backend is running.",
        "Check your internet connection.",
      ],
      technical: err.message,
    } satisfies GrowthOSError;
  }
}

interface StreamCallbacks {
  onToken?: (
    token: string
  ) => void;

  onArtifact?: (
    artifact: Artifact
  ) => void;

  onMessage?: (
    message: ChatMessage
  ) => void;

  onChatTitle?: (
    chat: {
      id: number;
      title: string;
    }
  ) => void;

  onDone?: () => void;

  onError?: (
    error: GrowthOSError
  ) => void;
}

export async function sendChatStream(
  payload: ChatRequest,
  callbacks: StreamCallbacks
) {
  const response = await fetch(
    "http://localhost:8000/api/v1/chat/stream",
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",

        Accept:
          "text/event-stream",
      },

      body: JSON.stringify(
        payload
      ),
    }
  );

  // -----------------------------
  // HTTP Error
  // -----------------------------

  if (!response.ok) {
    try {
      const body =
        await response.json();

      if (body.error) {
        callbacks.onError?.(
          body.error
        );
        return;
      }
    } catch {}

    callbacks.onError?.({
      title: "Request Failed",
      message:
        "The server returned an unexpected error.",
      suggestions: [
        "Try again.",
        "Check backend logs.",
      ],
      status_code:
        response.status,
    });

    return;
  }

  if (!response.body) {
    callbacks.onError?.({
      title:
        "Streaming Unsupported",
      message:
        "Your browser does not support streaming responses.",
      suggestions: [
        "Use a modern browser.",
      ],
    });

    return;
  }

  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();

  let buffer = "";

  while (true) {
    const {
      value,
      done,
    } = await reader.read();

    if (done) break;

    buffer += decoder.decode(
      value,
      {
        stream: true,
      }
    );

    const events =
      buffer.split("\n\n");

    buffer =
      events.pop() ?? "";

    for (const event of events) {
      let type = "";
      let data = "";

      for (const line of event.split(
        "\n"
      )) {
        if (
          line.startsWith(
            "event:"
          )
        ) {
          type = line
            .substring(6)
            .trim();
        }

        if (
          line.startsWith(
            "data:"
          )
        ) {
          data += line
            .substring(5)
            .trim();
        }
      }

      try {
        switch (type) {
          case "token":
            callbacks.onToken?.(
              data
            );
            break;

          case "artifact":
            callbacks.onArtifact?.(
              JSON.parse(data)
            );
            break;

          case "message":
            callbacks.onMessage?.(
              JSON.parse(data)
            );
            break;

          case "chat_title":
            callbacks.onChatTitle?.(
              JSON.parse(data)
            );
            break;

          case "error": {
            const payload =
              JSON.parse(data);

            callbacks.onError?.(
              payload.error ??
                payload
            );

            break;
          }

          case "done":
            callbacks.onDone?.();
            break;
        }
      } catch (err: any) {
        callbacks.onError?.({
          title:
            "Stream Parsing Error",
          message:
            "GrowthOS received an invalid streaming response.",
          suggestions: [
            "Try again.",
            "Restart the backend.",
          ],
          technical:
            err?.message,
        });
      }
    }
  }
}