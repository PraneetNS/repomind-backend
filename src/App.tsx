import RepoList from "./components/RepoList";

export default function App() {
  return (
    <div style={{ padding: "24px", fontFamily: "sans-serif" }}>
      <h1>RepoMind</h1>
      <p>AI-powered code understanding</p>

      <RepoList />
    </div>
  );
}
