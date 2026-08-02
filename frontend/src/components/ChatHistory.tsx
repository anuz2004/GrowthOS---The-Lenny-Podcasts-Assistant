import { useEffect, useRef } from "react";

import type { Message } from "../api/message";
import MessageBubble from "./MessageBubble";

interface Props {
  messages: Message[];
  loading: boolean;
}


export default function ChatHistory({
  messages,
  loading,
}: Props) {
  const bottomRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: 24,
      }}
    >
      {messages.length === 0 && (
        <div
          style={{
            marginTop: 140,
            textAlign: "center",
            color: "#6B7280",
          }}
        >
          GrowthOS Terminal Ready

          <br />
          <br />

          Ask anything.
        </div>
      )}

      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          content={message.content}
        />
      ))}

      {loading && (
        <MessageBubble
          role="assistant"
          content="Thinking..."
        />
      )}

      <div ref={bottomRef} />
    </div>
  );
}
