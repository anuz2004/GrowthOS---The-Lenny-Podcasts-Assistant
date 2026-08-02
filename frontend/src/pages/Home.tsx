import { useEffect, useState } from "react";
import { getWorkspaces, Workspace } from "../api/workspace";

export default function Home() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadWorkspaces();
  }, []);

  async function loadWorkspaces() {
    try {
      const data = await getWorkspaces();
      setWorkspaces(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>GrowthOS</h1>

      {workspaces.map((workspace) => (
        <div
          key={workspace.id}
          style={{
            padding: 15,
            marginBottom: 10,
            border: "1px solid #ccc",
            borderRadius: 8,
          }}
        >
          <h3>{workspace.title}</h3>
          <p>{workspace.description}</p>
        </div>
      ))}
    </div>
  );
}