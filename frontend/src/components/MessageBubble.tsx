import ReactMarkdown from "react-markdown";

interface MessageBubbleProps {
  role: string;
  content: string;
}

export default function MessageBubble({
  role,
  content,
}: MessageBubbleProps) {
  const isUser = role === "user";

  return (
    <div
      style={{
        padding: "22px 28px",
        borderBottom: "1px solid #1F2937",
        animation: "fadeIn 0.2s ease",
      }}
    >
      {/* Header */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          marginBottom: 16,
        }}
      >
        <div
          style={{
            color: isUser ? "#00FF9C" : "#3B82F6",
            fontWeight: 700,
            fontSize: 13,
            letterSpacing: 1,
          }}
        >
          {isUser ? "> USER" : "> GROWTHOS"}
        </div>

        <div
          style={{
            flex: 1,
            height: 1,
            background: "#1F2937",
          }}
        />
      </div>

      {/* Message */}

      {isUser ? (
        <pre
          style={{
            margin: 0,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
            color: "#FAFAFA",
            lineHeight: 1.8,
            fontFamily: "JetBrains Mono, monospace",
            fontSize: 15,
          }}
        >
          {content}
        </pre>
      ) : (
        <div
          style={{
            color: "#E5E7EB",
            lineHeight: 1.8,
            fontSize: 15,
          }}
        >
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}