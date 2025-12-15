import { useState } from "react";

export default function ChatUI() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function ask() {
    if (!query.trim()) return;

    setLoading(true);
    setAnswer("");

    const res = await fetch("/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setAnswer(data.answer);
    setLoading(false);
  }

  return (
    <div style={{ marginTop: "24px" }}>
      <h2>Ask your code</h2>

      <textarea
        rows={4}
        style={{ width: "100%" }}
        value={query}
        placeholder="Ask something about the codebase..."
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={ask} disabled={loading} style={{ marginTop: "8px" }}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <pre
          style={{
            marginTop: "16px",
            padding: "12px",
            background: "#111",
            color: "#0f0",
            whiteSpace: "pre-wrap",
          }}
        >
          {answer}
        </pre>
      )}
    </div>
  );
}
