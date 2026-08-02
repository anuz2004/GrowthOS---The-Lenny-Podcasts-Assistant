import type { CSSProperties, ReactNode } from "react";

interface Props {
  children: ReactNode;
  style?: CSSProperties;
}

export default function Panel({
  children,
  style,
}: Props) {
  return (
    <div
      style={{
        height: "100%",
        background: "#111217",
        border: "1px solid #27272A",
        borderRadius: 10,
        overflow: "hidden",
        ...style,
      }}
    >
      {children}
    </div>
  );
}