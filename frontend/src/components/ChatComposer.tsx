import { useEffect, useRef } from "react";

interface ChatComposerProps {
  value: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSend: () => void;
}

export default function ChatComposer({
  value,
  loading,
  onChange,
  onSend,
}: ChatComposerProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "48px";
    textarea.style.height = `${textarea.scrollHeight}px`;
  }, [value]);

  return (
    <div
      style={{
        borderTop: "1px solid #27272A",
        padding: 20,
        background: "#09090B",
      }}
    >
      <div
        style={{
          display: "flex",
          gap: 14,
          alignItems: "flex-end",
        }}
      >
        <div
          style={{
            color: "#00FF9C",
            fontSize: 18,
            fontWeight: 700,
            paddingBottom: 12,
          }}
        >
          ❯
        </div>

        <textarea
          ref={textareaRef}
          value={value}
          disabled={loading}
          placeholder="Ask GrowthOS..."
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
          style={{
            flex: 1,
            resize: "none",
            minHeight: 48,
            maxHeight: 220,
            overflow: "auto",

            background: "transparent",
            border: "none",
            outline: "none",

            color: "#FAFAFA",

            fontFamily: "JetBrains Mono, monospace",

            fontSize: 15,

            lineHeight: 1.7,
          }}
        />

        <button
          onClick={onSend}
          disabled={loading}
          style={{
            height: 48,
            width: 90,

            background: "#18181B",

            border: "1px solid #27272A",

            color: "#00FF9C",

            cursor: loading ? "not-allowed" : "pointer",

            fontFamily: "JetBrains Mono, monospace",
          }}
        >
          {loading ? "..." : "SEND"}
        </button>
      </div>
    </div>
  );
}