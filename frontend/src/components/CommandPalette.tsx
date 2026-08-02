import { useEffect, useMemo, useRef, useState } from "react";

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
  onSelect: (prompt: string) => void;
}

const COMMANDS = [
  {
    title: "README Generator",
    description: "Generate a professional README.md",
    prompt: "Generate a professional README.md for my project.",
  },
  {
    title: "PRD Generator",
    description: "Generate a Product Requirements Document",
    prompt: "Generate a Product Requirements Document.",
  },
  {
    title: "Architecture Document",
    description: "Generate a software architecture document",
    prompt: "Generate a software architecture document.",
  },
  {
    title: "Landing Page",
    description: "Generate a responsive landing page",
    prompt: "Generate a modern responsive landing page.",
  },
  {
    title: "React Component",
    description: "Generate a production-ready React component",
    prompt: "Generate a production-ready React component.",
  },
  {
    title: "Ship30 Essay",
    description: "Write in Ship30 style",
    prompt: "Write a Ship30 style article.",
  },
];

export default function CommandPalette({
  open,
  onClose,
  onSelect,
}: CommandPaletteProps) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(0);

  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();

    if (!q) return COMMANDS;

    return COMMANDS.filter(
      (cmd) =>
        cmd.title.toLowerCase().includes(q) ||
        cmd.description.toLowerCase().includes(q)
    );
  }, [query]);

  useEffect(() => {
    if (!open) return;

    setQuery("");
    setSelected(0);

    setTimeout(() => {
      inputRef.current?.focus();
    }, 10);
  }, [open]);

  useEffect(() => {
    if (!open) return;

    function handle(e: KeyboardEvent) {
      switch (e.key) {
        case "Escape":
          e.preventDefault();
          onClose();
          break;

        case "ArrowDown":
          e.preventDefault();
          setSelected((v) =>
            Math.min(v + 1, filtered.length - 1)
          );
          break;

        case "ArrowUp":
          e.preventDefault();
          setSelected((v) => Math.max(v - 1, 0));
          break;

        case "Enter":
          e.preventDefault();

          if (!filtered.length) return;

          onSelect(filtered[selected].prompt);
          onClose();
          break;
      }
    }

    window.addEventListener("keydown", handle);

    return () =>
      window.removeEventListener("keydown", handle);
  }, [open, filtered, selected, onClose, onSelect]);

  if (!open) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,.65)",
        backdropFilter: "blur(4px)",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        paddingTop: 120,
        zIndex: 9999,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: 700,
          background: "#111217",
          border: "1px solid #27272A",
          borderRadius: 12,
          overflow: "hidden",
          boxShadow: "0 30px 80px rgba(0,0,0,.45)",
          fontFamily: "JetBrains Mono, monospace",
        }}
      >
        {/* Header */}

        <div
          style={{
            padding: "18px 20px",
            borderBottom: "1px solid #27272A",
            color: "#00FF9C",
            fontWeight: 700,
            fontSize: 14,
          }}
        >
          GrowthOS Command Palette
        </div>

        {/* Search */}

        <div
          style={{
            padding: 16,
            borderBottom: "1px solid #27272A",
          }}
        >
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelected(0);
            }}
            placeholder="Search commands..."
            style={{
              width: "100%",
              background: "#18181B",
              border: "1px solid #27272A",
              borderRadius: 8,
              padding: "12px 14px",
              color: "#FAFAFA",
              outline: "none",
              fontFamily: "inherit",
              fontSize: 14,
            }}
          />
        </div>

        {/* Commands */}

        <div
          style={{
            maxHeight: 420,
            overflowY: "auto",
          }}
        >
          {filtered.length === 0 ? (
            <div
              style={{
                padding: 24,
                color: "#71717A",
                textAlign: "center",
              }}
            >
              No matching commands.
            </div>
          ) : (
            filtered.map((cmd, index) => (
              <div
                key={cmd.title}
                onMouseEnter={() => setSelected(index)}
                onClick={() => {
                  onSelect(cmd.prompt);
                  onClose();
                }}
                style={{
                  cursor: "pointer",
                  padding: "16px 18px",
                  background:
                    index === selected
                      ? "#18181B"
                      : "transparent",
                  borderLeft:
                    index === selected
                      ? "3px solid #00FF9C"
                      : "3px solid transparent",
                  transition: "all 150ms ease",
                }}
              >
                <div
                  style={{
                    color:
                      index === selected
                        ? "#00FF9C"
                        : "#FAFAFA",
                    fontWeight: 600,
                  }}
                >
                  {cmd.title}
                </div>

                <div
                  style={{
                    marginTop: 4,
                    color: "#71717A",
                    fontSize: 12,
                  }}
                >
                  {cmd.description}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: "12px 18px",
            borderTop: "1px solid #27272A",
            color: "#71717A",
            fontSize: 12,
          }}
        >
          <span>↑ ↓ Navigate</span>
          <span>Enter Select</span>
          <span>Esc Close</span>
        </div>
      </div>
    </div>
  );
}