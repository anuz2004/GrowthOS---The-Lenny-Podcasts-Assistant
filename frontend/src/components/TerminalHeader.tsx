interface TerminalHeaderProps {
  provider: string;
  model: string;
}

export default function TerminalHeader({
  provider,
  model,
}: TerminalHeaderProps) {
  return (
    <header
      style={{
        height: 64,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "0 24px",
        borderBottom: "1px solid #27272A",
        background: "#09090B",
        fontFamily: "JetBrains Mono, monospace",
      }}
    >
      <div>
        <div
          style={{
            color: "#FAFAFA",
            fontWeight: 700,
            fontSize: 18,
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
          v1.0
        </div>
      </div>

      <div
        style={{
          display: "flex",
          gap: 32,
          alignItems: "center",
          color: "#A1A1AA",
          fontSize: 13,
        }}
      >
        <div>
          Provider{" "}
          <span style={{ color: "#00FF9C" }}>
            {provider}
          </span>
        </div>

        <div>
          Model{" "}
          <span style={{ color: "#3B82F6" }}>
            {model}
          </span>
        </div>

        <div
          style={{
            color: "#00FF9C",
          }}
        >
          ● Connected
        </div>
      </div>
    </header>
  );
}