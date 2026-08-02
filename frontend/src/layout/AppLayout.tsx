import type {
  Artifact,
} from "../api/chat";
import type { GrowthOSError } from "../types/error";
import ArtifactViewer from "../components/ArtifactViewer";
import ChatWindow from "../components/ChatWindow";
import Sidebar from "../components/Sidebar";
import TopBar from "../components/TopBar";

interface AppLayoutProps {
  selectedWorkspace: number | null;
  onWorkspaceSelect: (id: number) => void;

  selectedSession: number | null;
  onSessionSelect: (id: number | null) => void;

  artifact: Artifact | null;
  onArtifactChange: (artifact: Artifact | null) => void;

  provider: string;
  onProviderChange: (provider: string) => void;

  model: string;
  onModelChange: (model: string) => void;

  // NEW
  onError: (
    error: GrowthOSError
  ) => void;
}

export default function AppLayout({
  selectedWorkspace,
  onWorkspaceSelect,
  selectedSession,
  onSessionSelect,
  artifact,
  onArtifactChange,
  provider,
  onProviderChange,
  model,
  onModelChange,
  onError,
}: AppLayoutProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "260px minmax(600px,1fr) 420px",
        gridTemplateRows: "64px 1fr",
        height: "100vh",
        background: "#09090B",
        color: "#FAFAFA",
        fontFamily:
          "JetBrains Mono, monospace",
      }}
    >
      {/* Header */}

      <header
        style={{
          gridColumn: "1 / -1",
          borderBottom:
            "1px solid #27272A",
          background: "#0D0D0D",
          zIndex: 20,
        }}
      >
        <TopBar
          workspace="GrowthOS"
          provider={provider}
          model={model}
          connected={true}
        />
      </header>

      {/* Sidebar */}

      <aside
        style={{
          borderRight:
            "1px solid #27272A",
          background: "#111217",
          overflow: "hidden",
        }}
      >
        <Sidebar
          selectedWorkspace={
            selectedWorkspace
          }
          onWorkspaceSelect={
            onWorkspaceSelect
          }
          selectedSession={
            selectedSession
          }
          onSessionSelect={
            onSessionSelect
          }
          provider={provider}
          onProviderChange={
            onProviderChange
          }
          model={model}
          onModelChange={
            onModelChange
          }
        />
      </aside>

      {/* Chat */}

      <main
        style={{
          background: "#09090B",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <ChatWindow
          workspaceId={
            selectedWorkspace
          }
          selectedSession={
            selectedSession
          }
          onSessionSelect={
            onSessionSelect
          }
          onArtifactChange={
            onArtifactChange
          }

          onError={onError}
        />
      </main>

      {/* Artifact */}

      <aside
        style={{
          borderLeft:
            "1px solid #27272A",
          background: "#111217",
          overflow: "hidden",
        }}
      >
        <ArtifactViewer
          artifact={artifact}
        />
      </aside>
    </div>
  );
}