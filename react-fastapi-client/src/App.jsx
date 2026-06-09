import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const API_BASE_URL = "https://potential-winner-jj4g5rw649492596-8000.app.github.dev";

  async function askFastApi(message) {
    const response = await fetch(`${API_BASE_URL}/api/ai/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message
      })
    });

    if (!response.ok) {
      throw new Error("FastAPI 서버 요청에 실패했습니다.");
    }

    const result = await response.json();

    return result.data.answer;
  }

  async function handleAsk() {
    if (!message.trim()) {
      alert("질문을 입력하세요.");
      return;
    }

    try {
      setLoading(true);
      setAnswer("");
      setError("");

      const result = await askFastApi(message);

      setAnswer(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: "30px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>React에서 FastAPI AI 호출</h1>

      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="질문을 입력하세요"
        rows={5}
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "16px"
        }}
      />

      <br />
      <br />

      <button
        onClick={handleAsk}
        disabled={loading}
        style={{
          padding: "10px 20px",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "응답 생성 중..." : "FastAPI에 질문하기"}
      </button>

      <hr />

      <h2>AI 응답</h2>

      {loading && <p>AI 응답을 생성하고 있습니다.</p>}

      {error && (
        <p style={{ color: "red" }}>
          오류: {error}
        </p>
      )}

      {!loading && answer && (
        <div
          style={{
            whiteSpace: "pre-wrap",
            border: "1px solid #ddd",
            padding: "15px",
            borderRadius: "8px"
          }}
        >
          {answer}
        </div>
      )}
    </div>
  );
}

export default App;