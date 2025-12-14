import { useState } from "react";

export default function CreateRepo({
  onCreated,
}: {
  onCreated: () => void;
}) {
  const [name, setName] = useState("");
  const [path, setPath] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    if (!name || !path) {
      setError("Name and path are required");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/repos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, path }),
      });

      if (!res.ok) {
        throw new Error("Failed to create repo");
      }

      setName("");
      setPath("");
      onCreated();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ marginBottom: "24px" }}>
      <h2>Add Repository</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <input
        placeholder="Repo name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ display: "block", marginBottom: "8px" }}
      />

      <input
        placeholder="Absolute local path"
        value={path}
        onChange={(e) => setPath(e.target.value)}
        style={{ display: "block", marginBottom: "8px", width: "420px" }}
      />

      <button onClick={submit} disabled={loading}>
        {loading ? "Indexing..." : "Create & Index"}
      </button>
    </div>
  );
}
