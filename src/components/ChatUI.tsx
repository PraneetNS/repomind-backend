import { useState } from "react";

export default function Chat() {
  const [q, setQ] = useState("");
  const [a, setA] = useState("");

  async function ask() {
    const res = await fetch("/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q }),
    });
    const data = await res.json();
    setA(data.answer);
  }

  return (
    <div style={{ marginTop: "32px" }}>
      <h2>Ask your code</h2>
      <textarea
        rows={4}
        value={q}
        onChange={(e) => setQ(e.target.value)}
        style={{ width: "100%" }}
      />
      <button onClick={ask}>Ask</button>

      {a && (
        <pre style={{ marginTop: "16px", background: "#111", color: "#0f0", padding: "12px" }}>
          {a}
        </pre>
      )}
    </div>
  );
}
