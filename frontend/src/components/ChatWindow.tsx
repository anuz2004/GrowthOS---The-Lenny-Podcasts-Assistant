import { useEffect, useState } from "react";

import {
  sendChatStream,
  type Artifact,
  type ChatMessage,
} from "../api/chat";
import type { GrowthOSError } from "../types/error";

import {
  getMessages,
  type Message,
} from "../api/message";

import ChatComposer from "./ChatComposer";
import ChatHistory from "./ChatHistory";

interface Props {
  workspaceId: number | null;

  selectedSession: number | null;

  onSessionSelect: (
    id: number | null
  ) => void;

  onArtifactChange: (
    artifact: Artifact | null
  ) => void;

  onTitleChange?: (
    chat: {
      id: number;
      title: string;
    }
  ) => void;

  onError: (
    error: GrowthOSError
  ) => void;
}

export default function ChatWindow({
  selectedSession,
  onArtifactChange,
  onTitleChange,
  onError,
}: Props) {
  const [messages, setMessages] =
    useState<Message[]>([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  useEffect(() => {
    if (selectedSession !== null) {
      loadMessages(selectedSession);
    } else {
      setMessages([]);
    }
  }, [selectedSession]);

  async function loadMessages(
    sessionId: number
  ) {
    try {
      const data =
        await getMessages(sessionId);

      setMessages(data);
    } catch (err) {
      console.error(err);
    }
  }

  async function sendMessage() {
    if (
      !selectedSession ||
      !input.trim() ||
      loading
    ) {
      return;
    }

    const prompt = input.trim();

    setInput("");
    setLoading(true);

    const userId = Date.now();

    const assistantId =
      Date.now() + 1;

    const now =
      new Date().toISOString();

    const userMessage: Message = {
      id: userId,
      role: "user",
      content: prompt,
      created_at: now,
    };

    const assistantMessage: Message = {
      id: assistantId,
      role: "assistant",
      content: "",
      created_at: now,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      assistantMessage,
    ]);

    try {
      await sendChatStream(
        {
          chat_session_id:
            selectedSession,
          message: prompt,
        },
        {
          onToken(token) {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId
                  ? {
                      ...m,
                      content:
                        m.content +
                        token,
                    }
                  : m
              )
            );
          },

          onArtifact(
            artifact
          ) {
            onArtifactChange(
              artifact
            );
          },

          onMessage(
            message: ChatMessage
          ) {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantId
                  ? message
                  : m
              )
            );
          },

          onChatTitle(chat) {
            onTitleChange?.(chat);
          },

          onDone() {
            setLoading(false);

            window.dispatchEvent(
              new Event(
                "growthos-refresh-sessions"
              )
            );
          },

          onError(error) {
            setLoading(false);

            onError(error);
          },
        }
      );
    } catch (err) {
      setLoading(false);

      if (
        err &&
        typeof err === "object" &&
        "title" in err
      ) {
        onError(
          err as GrowthOSError
        );
      } else {
        onError({
          title: "Unexpected Error",
          message:
            err instanceof Error
              ? err.message
              : "Something went wrong while sending your message.",
          suggestions: [
            "Please try again.",
            "Verify the backend server is running.",
          ],
          technical:
            err instanceof Error
              ? err.stack
              : undefined,
        });
      }
    }
  }

  return (
    <>
      <ChatHistory
        messages={messages}
        loading={loading}
      />

      <ChatComposer
        value={input}
        loading={loading}
        onChange={setInput}
        onSend={sendMessage}
      />
    </>
  );
}