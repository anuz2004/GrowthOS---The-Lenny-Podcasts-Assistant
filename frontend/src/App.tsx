import { useState } from "react";

import type { Artifact } from "./api/chat";
import type { GrowthOSError } from "./types/error";

import ErrorDialog from "./components/ErrorDialog";
import AppLayout from "./layout/AppLayout";

function App() {
  const [selectedWorkspace, setSelectedWorkspace] =
    useState<number | null>(null);

  const [selectedSession, setSelectedSession] =
    useState<number | null>(null);

  const [artifact, setArtifact] =
    useState<Artifact | null>(null);

  const [provider, setProvider] =
    useState("ollama");

  const [model, setModel] =
    useState("qwen3:8b");

  const [error, setError] =
    useState<GrowthOSError | null>(null);

  return (
    <>
      <AppLayout
        selectedWorkspace={selectedWorkspace}
        onWorkspaceSelect={setSelectedWorkspace}
        selectedSession={selectedSession}
        onSessionSelect={setSelectedSession}
        artifact={artifact}
        onArtifactChange={setArtifact}
        provider={provider}
        onProviderChange={setProvider}
        model={model}
        onModelChange={setModel}
        onError={setError}
      />

      <ErrorDialog
        error={error}
        onClose={() => setError(null)}
      />
    </>
  );
}

export default App;