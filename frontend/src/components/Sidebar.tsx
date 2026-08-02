import {
  useEffect,
  useRef,
  useState,
} from "react";
import {
  createChatSession,
  deleteChatSession,
  getChatSessions,
  type ChatSession,
} from "../api/session";

import {
  deleteWorkspace,
  getWorkspaces,
  type Workspace,
} from "../api/workspace";
import CreateWorkspaceModal from "./CreateWorkspaceModal";
import { createWorkspace } from "../api/workspace";

interface SidebarProps {
  selectedWorkspace: number | null;
  onWorkspaceSelect: (id: number) => void;

  selectedSession: number | null;
  onSessionSelect: (id: number | null) => void;

  provider: string;
  onProviderChange: (provider: string) => void;

  model: string;
  onModelChange: (model: string) => void;
}

const MODELS: Record<string, string[]> = {
  ollama: [
    "qwen3:8b",
    "llama3.2:3b",
    "phi4",
    "gemma3:4b",
    "mistral",
  ],

  openai: [
    "gpt-4.1",
    "gpt-4o",
    "gpt-4.1-mini",
  ],

  anthropic: [
    "claude-sonnet-4-20250514",
    "claude-opus-4-20250514",
  ],

  grok: [
    "grok-4",
    "grok-3",
    "grok-3-mini",
  ],
  groq: [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "deepseek-r1-distill-llama-70b",
    "qwen/qwen3-32b",
    "gemma2-9b-it",
  ],
};

const PROVIDER_LABELS: Record<string, string> = {
  ollama: "Ollama",
  openai: "OpenAI",
  anthropic: "Claude",
  grok: "Grok (xAI)",
  groq: "Groq",
};

export default function Sidebar({
  selectedWorkspace,
  onWorkspaceSelect,
  selectedSession,
  onSessionSelect,

  provider,
  onProviderChange,

  model,
  onModelChange,
}: SidebarProps) {
  const [showWorkspaceModal, setShowWorkspaceModal] =
  useState(false);

const [creatingWorkspace, setCreatingWorkspace] =
  useState(false);
  const [workspaces, setWorkspaces] =
    useState<Workspace[]>([]);

  const [sessions, setSessions] =
    useState<ChatSession[]>([]);

  const [creating, setCreating] =
    useState(false);

  useEffect(() => {
    loadWorkspaces();
  }, []);

  useEffect(() => {
    if (selectedWorkspace !== null) {
      loadSessions();
    } else {
      setSessions([]);
    }
  }, [selectedWorkspace]);
  
  useEffect(() => {
  function refreshSessions() {
    if (selectedWorkspace !== null) {
      loadSessions();
    }
  }

  window.addEventListener(
    "growthos-refresh-sessions",
    refreshSessions
  );

  return () =>
    window.removeEventListener(
      "growthos-refresh-sessions",
      refreshSessions
    );
}, [selectedWorkspace]);

  async function loadWorkspaces() {
    try {
      const data = await getWorkspaces();

      setWorkspaces(data);

      if (
        data.length > 0 &&
        selectedWorkspace === null
      ) {
        onWorkspaceSelect(data[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  }

 async function loadSessions() {
  try {
    const data = await getChatSessions();

    const filtered = data.filter(
      (s) =>
        s.workspace_id === selectedWorkspace
    );

    setSessions(filtered);

    // Auto-select only on first load.
    if (
      selectedSession === null &&
      filtered.length > 0
    ) {
      onSessionSelect(filtered[0].id);
    }
  } catch (err) {
    console.error(err);
  }
}

  async function handleNewChat() {
    if (
      selectedWorkspace === null ||
      creating
    )
      return;

    try {
      setCreating(true);

      const session =
        await createChatSession({
          workspace_id:
            selectedWorkspace,

          title: "New Chat",

          provider,

          model,
        });

      await loadSessions();

      onSessionSelect(session.id);
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  }
  async function handleCreateWorkspace(
  title: string,
  description: string
) {
  try {
    setCreatingWorkspace(true);

    const workspace =
      await createWorkspace({
        title,
        description,
        icon: "📁",
        color: "#00FF9C",
        default_model: model,
        mode: "default",
      });

    await loadWorkspaces();

onWorkspaceSelect(workspace.id);

setSessions([]);

onSessionSelect(null);

setShowWorkspaceModal(false);

  } catch (err) {
    console.error(err);
  } finally {
    setCreatingWorkspace(false);
  }
}
  async function handleDeleteChat(
  sessionId: number
) {
  const ok = window.confirm(
    "Delete this chat?"
  );

  if (!ok) return;

  try {
    await deleteChatSession(
      sessionId
    );

    await loadSessions();

    if (
      selectedSession ===
      sessionId
    ) {
      onSessionSelect(
        sessions.length > 1
          ? sessions.find(
              (s) =>
                s.id !== sessionId
            )?.id ?? null
          : null
      );
    }
  } catch (err) {
    console.error(err);
  }
}

async function handleDeleteWorkspace(
  workspaceId: number
) {
  const ok = window.confirm(
    "Delete this workspace?\n\nAll chats inside it will also be deleted."
  );

  if (!ok) return;

  try {
    await deleteWorkspace(
      workspaceId
    );

    await loadWorkspaces();

    setSessions([]);

    onWorkspaceSelect(
      workspaces.find(
        (w) =>
          w.id !== workspaceId
      )?.id ?? 0
    );

    onSessionSelect(null);
  } catch (err) {
    console.error(err);
  }
}

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        minHeight: 0,
        overflow: "hidden",
        padding: 20,
        background: "#111217",
        color: "#FAFAFA",
        fontFamily:
          "JetBrains Mono, monospace",
      }}
    >
      <CreateWorkspaceModal
      open={showWorkspaceModal}
      loading={creatingWorkspace}
      onClose={() =>
        setShowWorkspaceModal(false)
      }
      onCreate={handleCreateWorkspace}
    />
      {/* Header

      <div
        style={{
          marginBottom: 28,
        }}
      >
        <div
          style={{
            fontWeight: 700,
            fontSize: 20,
          }}
        >
          growthos@
          {provider}
        </div>

        <div
          style={{
            color: "#00FF9C",
            marginTop: 8,
            fontSize: 12,
          }}
        >
          ● Connected
        </div>

        <div
          style={{
            marginTop: 14,
            fontSize: 12,
            color: "#A1A1AA",
            lineHeight: 1.7,
          }}
        >
          Provider
          <br />
          <span
            style={{
              color: "#FAFAFA",
            }}
          >
            {
              PROVIDER_LABELS[
                provider
              ]
            }
          </span>

          <br />
          <br />

          Model
          <br />
          <span
            style={{
              color: "#00FF9C",
            }}
          >
            {model}
          </span>
        </div>
      </div>

      <Divider /> */}

      {/* Workspaces */}

      <SectionTitle title="WORKSPACES" />
      <button
  onClick={() =>
    setShowWorkspaceModal(true)
  }
  style={{
    width: "100%",
    height: 42,
    marginBottom: 16,

    borderRadius: 8,

    background: "#18181B",

    border: "1px solid #27272A",

    color: "#00FF9C",

    cursor: "pointer",

    fontFamily:
      "JetBrains Mono",
  }}
>
  + New Workspace
</button>

<div
  style={{
    maxHeight: 180,
    overflowY: "auto",
    paddingRight: 4,
  }}
>
  {workspaces.map((workspace) => (
    <SidebarItem
    key={workspace.id}
    active={
        workspace.id ===
        selectedWorkspace
    }
    text={workspace.title}
    onClick={() =>
        onWorkspaceSelect(
            workspace.id
        )
    }
    onRename={() => {}}
    onDelete={() =>
        handleDeleteWorkspace(
            workspace.id
        )
    }
/>
  ))}
</div>

      <Divider />

      {/* Provider */}

      <SectionTitle title="PROVIDER" />

      <select
        value={provider}
        onChange={(e) => {
          const value =
            e.target.value;

          onProviderChange(value);

          onModelChange(
              MODELS[value][0]
          );
        }}
        style={selectStyle}
      >
        <option value="ollama">
          Ollama
        </option>

        <option value="openai">
          OpenAI
        </option>

        <option value="anthropic">
          Claude
        </option>

        <option value="grok">
          Grok (xAI)
        </option>

        <option value="groq">
          Groq
        </option>
      </select>

      <SectionTitle title="MODEL" />

      <select
        value={model}
        onChange={(e) =>
          onModelChange(
            e.target.value
          )
        }
        style={selectStyle}
      >
        {MODELS[
          provider
        ].map((m) => (
          <option
            key={m}
            value={m}
          >
            {m}
          </option>
        ))}
      </select>

      <Divider />

            {/* Chats */}

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          flex: 1,
          minHeight: 0,
          marginTop: 8,
        }}
      >
        <SectionTitle title="CHATS" />

        <div
          style={{
            flex: 1,
            overflowY: "auto",
            paddingRight: 4,
          }}
        >
          {sessions.length === 0 ? (
            <div
              style={{
                color: "#71717A",
                fontSize: 13,
                padding: 12,
              }}
            >
              No chats yet.
            </div>
          ) : (
            sessions.map((session) => (
              <SidebarItem
    key={session.id}
    active={
        session.id ===
        selectedSession
    }
    text={session.title}
    onClick={() =>
        onSessionSelect(
            session.id
        )
    }
    onRename={() => {}}
    onDelete={() =>
        handleDeleteChat(
            session.id
        )
    }
/>
            ))
          )}
        </div>

        <div
          style={{
            marginTop: 16,
            paddingTop: 16,
            borderTop:
              "1px solid #27272A",
          }}
        >
          <button
            onClick={handleNewChat}
            disabled={
              creating ||
              selectedWorkspace === null
            }
            style={{
              width: "100%",
              height: 48,

              borderRadius: 8,

              border:
                "1px solid #27272A",

              background: "#18181B",

              color: "#00FF9C",

              cursor: creating
                ? "not-allowed"
                : "pointer",

              fontFamily: "inherit",

              fontWeight: 700,

              transition: "all .2s",
            }}
          >
            {creating
              ? "Creating..."
              : "+ New Chat"}
          </button>
        </div>
      </div>
    </div>
  );
}

function SectionTitle({
  title,
}: {
  title: string;
}) {
  return (
    <div
      style={{
        color: "#71717A",
        fontSize: 11,
        letterSpacing: 2,
        marginBottom: 12,
        marginTop: 18,
      }}
    >
      {title}
    </div>
  );
}

function Divider() {
  return (
    <div
      style={{
        borderTop:
          "1px solid #27272A",
        margin: "22px 0",
      }}
    />
  );
}

function SidebarItem({
  active,
  text,
  onClick,
  onRename,
  onDelete,
}: {
  active: boolean;
  text: string;
  onClick: () => void;
  onRename?: () => void;
  onDelete?: () => void;
}) {
  const [menuOpen, setMenuOpen] =
    useState(false);

  const menuRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (
        menuRef.current &&
        !menuRef.current.contains(
          e.target as Node
        )
      ) {
        setMenuOpen(false);
      }
    }

    window.addEventListener(
      "click",
      handleClick
    );

    return () =>
      window.removeEventListener(
        "click",
        handleClick
      );
  }, []);

  return (
    <div
      style={{
        position: "relative",
        marginBottom: 6,
      }}
    >
      <div
        onClick={onClick}
        style={{
          cursor: "pointer",
          padding: "10px 12px",
          borderRadius: 8,
          background: active
            ? "#18181B"
            : "transparent",
          color: active
            ? "#00FF9C"
            : "#FAFAFA",
          transition: "all .2s",
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center",
        }}
      >
        <span
          style={{
            overflow: "hidden",
            textOverflow:
              "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {active ? "▶ " : ""}
          {text}
        </span>

        {(onRename ||
          onDelete) && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setMenuOpen(
                !menuOpen
              );
            }}
            style={{
              background:
                "transparent",
              border: "none",
              color: "#71717A",
              cursor: "pointer",
              fontSize: 18,
              padding: "0 6px",
            }}
          >
            ⋮
          </button>
        )}
      </div>

      {menuOpen && (
        <div
          ref={menuRef}
          style={{
            position: "absolute",
            top: 38,
            right: 0,
            width: 140,
            background:
              "#18181B",
            border:
              "1px solid #27272A",
            borderRadius: 8,
            overflow: "hidden",
            zIndex: 100,
          }}
        >
          {onRename && (
            <MenuItem
              text="Rename"
              onClick={() => {
                setMenuOpen(
                  false
                );
                onRename();
              }}
            />
          )}

          {onDelete && (
            <MenuItem
              text="Delete"
              danger
              onClick={() => {
                setMenuOpen(
                  false
                );
                onDelete();
              }}
            />
          )}
        </div>
      )}
    </div>
  );
}
function MenuItem({
  text,
  danger,
  onClick,
}: {
  text: string;
  danger?: boolean;
  onClick: () => void;
}) {
  return (
    <div
      onClick={onClick}
      style={{
        padding: "10px 14px",
        cursor: "pointer",
        color: danger
          ? "#EF4444"
          : "#FAFAFA",
        borderBottom:
          "1px solid #27272A",
      }}
    >
      {text}
    </div>
  );
}

const selectStyle: React.CSSProperties = {
  width: "100%",
  padding: "10px",
  marginBottom: 10,
  background: "#18181B",
  color: "#FAFAFA",
  border: "1px solid #27272A",
  borderRadius: 8,
  fontFamily:
    "JetBrains Mono, monospace",
};