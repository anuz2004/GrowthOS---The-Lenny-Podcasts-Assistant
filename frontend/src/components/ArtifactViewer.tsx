import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Prism as SyntaxHighlighter,
} from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import type { Artifact } from "../api/chat";

interface Props {
  artifact: Artifact | null;
}

export default function ArtifactViewer({
  artifact,
}: Props) {
  const [view, setView] = useState<"preview" | "code">("preview");

  if (!artifact) {
    return (
      <div
        style={{
          height: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "#111217",
          color: "#71717A",
          fontFamily: "JetBrains Mono",
          fontSize: 14,
        }}
      >
        Waiting for artifact...
      </div>
    );
  }

  function copyArtifact() {
    navigator.clipboard.writeText(artifact.content);
  }

  function downloadArtifact() {
    const blob = new Blob(
      [artifact.content],
      { type: "text/plain" }
    );

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;
    a.download = artifact.title;

    a.click();

    URL.revokeObjectURL(url);
  }

  function detectLanguage() {
    const title = artifact.title.toLowerCase();

    if (title.endsWith(".tsx")) return "tsx";
    if (title.endsWith(".ts")) return "typescript";
    if (title.endsWith(".js")) return "javascript";
    if (title.endsWith(".jsx")) return "jsx";
    if (title.endsWith(".py")) return "python";
    if (title.endsWith(".java")) return "java";
    if (title.endsWith(".json")) return "json";
    if (title.endsWith(".css")) return "css";
    if (title.endsWith(".html")) return "html";
    if (title.endsWith(".sql")) return "sql";
    if (title.endsWith(".md")) return "markdown";

    return "text";
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: "#111217",
      }}
    >
      {/* Header */}

      <div
        style={{
          padding: 18,
          borderBottom: "1px solid #27272A",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div>
            <div
              style={{
                color: "#FAFAFA",
                fontWeight: 700,
                fontSize: 17,
              }}
            >
              {artifact.title}
            </div>

            <div
              style={{
                marginTop: 4,
                color: "#71717A",
                fontSize: 12,
              }}
            >
              {artifact.type.toUpperCase()}
            </div>
          </div>

          <div
            style={{
              display: "flex",
              gap: 8,
            }}
          >
            <ToolbarButton onClick={copyArtifact}>
              Copy
            </ToolbarButton>

            <ToolbarButton onClick={downloadArtifact}>
              Download
            </ToolbarButton>
          </div>
        </div>

        <div
          style={{
            display: "flex",
            gap: 8,
            marginTop: 18,
          }}
        >
          <TabButton
            active={view === "preview"}
            onClick={() => setView("preview")}
          >
            Preview
          </TabButton>

          <TabButton
            active={view === "code"}
            onClick={() => setView("code")}
          >
            Source
          </TabButton>
        </div>
      </div>

      {/* Body */}

      <div
        style={{
          flex: 1,
          overflow: "auto",
          background: "#0D1117",
        }}
      >
        {view === "preview" ? (
          artifact.type === "html" ? (
            <iframe
              srcDoc={artifact.content}
              title="preview"
              style={{
                width: "100%",
                height: "100%",
                border: "none",
                background: "#FFF",
              }}
            />
          ) : artifact.type === "markdown" ? (
            <div
              style={{
                padding: 30,
                color: "#FAFAFA",
              }}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
              >
                {artifact.content}
              </ReactMarkdown>
            </div>
          ) : (
            <SyntaxHighlighter
              language={detectLanguage()}
              style={oneDark}
              customStyle={{
                margin: 0,
                padding: 28,
                background: "#0D1117",
                minHeight: "100%",
                fontSize: 14,
              }}
            >
              {artifact.content}
            </SyntaxHighlighter>
          )
        ) : (
          <SyntaxHighlighter
            language={detectLanguage()}
            style={oneDark}
            customStyle={{
              margin: 0,
              padding: 28,
              background: "#0D1117",
              minHeight: "100%",
              fontSize: 14,
            }}
          >
            {artifact.content}
          </SyntaxHighlighter>
        )}
      </div>
    </div>
  );
}

function TabButton({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "8px 14px",
        border: "1px solid #27272A",
        background: active ? "#00FF9C" : "#18181B",
        color: active ? "#000" : "#FAFAFA",
        borderRadius: 6,
        cursor: "pointer",
        fontFamily: "JetBrains Mono",
        transition: "150ms",
      }}
    >
      {children}
    </button>
  );
}

function ToolbarButton({
  onClick,
  children,
}: {
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "8px 12px",
        border: "1px solid #27272A",
        background: "#18181B",
        color: "#FAFAFA",
        borderRadius: 6,
        cursor: "pointer",
        fontFamily: "JetBrains Mono",
        transition: "150ms",
      }}
    >
      {children}
    </button>
  );
}