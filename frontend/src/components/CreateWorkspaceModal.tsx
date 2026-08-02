import { useState } from "react";

interface Props {
  open: boolean;
  loading: boolean;

  onClose: () => void;

  onCreate: (
    title: string,
    description: string
  ) => void;
}

export default function CreateWorkspaceModal({
  open,
  loading,
  onClose,
  onCreate,
}: Props) {
  const [title, setTitle] =
    useState("");

  const [description, setDescription] =
    useState("");

  if (!open) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,.65)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 999,
      }}
    >
      <div
        style={{
          width: 420,
          background: "#111217",
          border: "1px solid #27272A",
          borderRadius: 12,
          padding: 24,
        }}
      >
        <h2
          style={{
            marginTop: 0,
            color: "#FAFAFA",
          }}
        >
          New Workspace
        </h2>

        <input
          placeholder="Workspace name"
          value={title}
          onChange={(e) =>
            setTitle(e.target.value)
          }
          style={inputStyle}
        />

        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) =>
            setDescription(
              e.target.value
            )
          }
          style={{
            ...inputStyle,
            minHeight: 100,
            resize: "none",
          }}
        />

        <div
          style={{
            display: "flex",
            justifyContent:
              "flex-end",
            gap: 12,
            marginTop: 20,
          }}
        >
          <button
            onClick={onClose}
            style={buttonStyle}
          >
            Cancel
          </button>

          <button
            disabled={
              loading ||
              !title.trim()
            }
            onClick={() => {
              onCreate(
                title,
                description
              );

              setTitle("");
              setDescription("");
            }}
            style={{
              ...buttonStyle,
              color: "#00FF9C",
            }}
          >
            Create
          </button>
        </div>
      </div>
    </div>
  );
}

const inputStyle: React.CSSProperties =
  {
    width: "100%",
    marginTop: 16,
    padding: 12,
    borderRadius: 8,
    border: "1px solid #27272A",
    background: "#18181B",
    color: "#FAFAFA",
    fontFamily:
      "JetBrains Mono",
    boxSizing: "border-box",
  };

const buttonStyle: React.CSSProperties =
  {
    padding: "10px 18px",
    background: "#18181B",
    border: "1px solid #27272A",
    borderRadius: 8,
    color: "#FAFAFA",
    cursor: "pointer",
  };