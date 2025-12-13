import { useEffect, useState } from "react";

type Repo = {
  id: number;
  name: string;
  path: string;
};

export default function RepoList() {
  const [repos, setRepos] = useState<Repo[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/repos")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch repos");
        return res.json();
      })
      .then(setRepos)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div style={{ marginTop: "16px" }}>
      <h2>Repositories</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {!error && repos.length === 0 && <p>No repos indexed yet</p>}

      <ul>
        {repos.map((r) => (
          <li key={r.id}>
            <strong>{r.name}</strong> — {r.path}
          </li>
        ))}
      </ul>
    </div>
  );
}
