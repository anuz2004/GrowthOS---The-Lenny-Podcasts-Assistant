interface TopBarProps {
  workspace?: string;
  provider?: string;
  model?: string;
  connected?: boolean;
}

export default function TopBar({
  workspace = "GrowthOS",
  provider = "Ollama",
  model = "qwen3:8b",
  connected = true,
}: TopBarProps) {
  return (
    <header
      style={{
        height: "100%",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0 24px",
        background: "#0D1117",
        borderBottom: "1px solid #27272A",
        fontFamily: "JetBrains Mono, monospace",
      }}
    >
      {/* Left */}

      <div>
        <div
          style={{
            fontSize: 18,
            fontWeight: 700,
            color: "#FAFAFA",
          }}
        >
          GrowthOS Terminal
        </div>

        <div
          style={{
            marginTop: 4,
            color: "#71717A",
            fontSize: 12,
          }}
        >
          AI Workspace
        </div>
      </div>

      {/* Center */}

      <div
        style={{
          display: "flex",
          gap: 28,
          fontSize: 13,
          color: "#A1A1AA",
        }}
      >
        <span>
          Workspace{" "}
          <span style={{ color: "#FAFAFA" }}>
            {workspace}
          </span>
        </span>

        <span>
          Provider{" "}
          <span style={{ color: "#00FF9C" }}>
            {provider}
          </span>
        </span>

        <span>
          Model{" "}
          <span style={{ color: "#3B82F6" }}>
            {model}
          </span>
        </span>
      </div>

      {/* Right */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          fontSize: 13,
          color: connected ? "#00FF9C" : "#EF4444",
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: connected ? "#00FF9C" : "#EF4444",
          }}
        />

        {connected ? "Connected" : "Offline"}
      </div>
    </header>
  );
}