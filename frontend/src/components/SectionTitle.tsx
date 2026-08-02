interface Props {
  title: string;
}

export default function SectionTitle({
  title,
}: Props) {
  return (
    <div
      style={{
        color: "#71717A",
        fontSize: 12,
        letterSpacing: 2,
        fontWeight: 700,
        marginBottom: 16,
      }}
    >
      {title}
    </div>
  );
}