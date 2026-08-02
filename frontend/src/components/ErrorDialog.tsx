import { theme } from "../styles/theme";

export interface GrowthOSError {
  title: string;
  message: string;
  suggestions: string[];
  technical?: string;
  status_code?: number;
}

interface Props {
  error: GrowthOSError | null;
  onClose: () => void;
}

export default function ErrorDialog({
  error,
  onClose,
}: Props) {
  if (!error) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,.75)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 9999,
      }}
    >
      <div
        style={{
          width: 560,
          background: theme.panel,
          border: `1px solid ${theme.danger}`,
          borderRadius: theme.radius,
          padding: 24,
        }}
      >
        <h2
          style={{
            color: theme.danger,
            marginBottom: 16,
          }}
        >
          ❌ {error.title}
        </h2>

        <p
          style={{
            color: theme.text,
            marginBottom: 20,
            lineHeight: 1.7,
          }}
        >
          {error.message}
        </p>

        {error.suggestions.length > 0 && (
          <>
            <div
              style={{
                color: theme.success,
                marginBottom: 10,
                fontWeight: 600,
              }}
            >
              What you can do
            </div>

            <ul
              style={{
                paddingLeft: 20,
                lineHeight: 1.8,
                color: theme.textSecondary,
              }}
            >
              {error.suggestions.map(
                (item, index) => (
                  <li key={index}>{item}</li>
                )
              )}
            </ul>
          </>
        )}

        {error.technical && (
          <details
            style={{
              marginTop: 24,
            }}
          >
            <summary
              style={{
                cursor: "pointer",
                color: theme.info,
              }}
            >
              Technical Details
            </summary>

            <pre
              style={{
                marginTop: 12,
                padding: 12,
                background: theme.panelAlt,
                border: `1px solid ${theme.border}`,
                color: theme.textSecondary,
                overflowX: "auto",
                whiteSpace: "pre-wrap",
              }}
            >
              {error.technical}
            </pre>
          </details>
        )}

        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            marginTop: 24,
          }}
        >
          <button
            onClick={onClose}
            style={{
              padding: "10px 18px",
              background: theme.button,
              color: theme.text,
              border: `1px solid ${theme.border}`,
              borderRadius: theme.radius,
            }}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}