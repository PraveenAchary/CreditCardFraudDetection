import { useState, useEffect } from "react";
import React from "react";

export default function Predict() {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("");
  const [time, setTime] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false); // ✅ Loading state
  const [progress, setProgress] = useState(0);   // ✅ Progress bar
  const [error, setError] = useState(null);

  // 🔥 Full dark theme
  useEffect(() => {
    document.body.style.margin = "0";
    document.body.style.backgroundColor = "#020617";
    document.body.style.color = "#e5e7eb";
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setProgress(0);
    setResult(null);
    setError(null);

    // Animate progress bar while waiting
    let prog = 0;
    const interval = setInterval(() => {
      prog += Math.random() * 10; // random progress increment
      if (prog > 95) prog = 95;    // stop before 100%
      setProgress(prog);
    }, 300);

    const dataToSend = {
      time: time,
      amount: amount,
    };

    try {
      const response = await fetch(
        "https://creditcardfrauddetection-firf.onrender.com/predict/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dataToSend),
        }
      );

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();
      setResult(data.prediction);
      setProgress(100); // complete progress bar
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      clearInterval(interval);
      setTimeout(() => setProgress(0), 500); // reset progress bar
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#020617",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          background: "#0f172a",
          padding: "32px 36px",
          borderRadius: "14px",
          width: "400px",
          boxShadow: "0 20px 40px rgba(0,0,0,0.7)",
          textAlign: "center",
          border: "1px solid #1f2937",
        }}
      >
        <h1 style={{ marginBottom: "22px" }}>Credit Card Fraud Detection</h1>

        <form onSubmit={handleSubmit}>
          {/* Name */}
          <div style={{ marginBottom: "18px", textAlign: "left" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "11px",
                marginTop: "6px",
                borderRadius: "7px",
                border: "1px solid #334155",
                fontSize: "14px",
                background: "#020617",
                color: "#e5e7eb",
              }}
            />
          </div>

          {/* Time */}
          <div style={{ marginBottom: "18px", textAlign: "left" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>Time</label>
            <input
              type="number"
              value={time}
              onChange={(e) => setTime(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "11px",
                marginTop: "6px",
                borderRadius: "7px",
                border: "1px solid #334155",
                fontSize: "14px",
                background: "#020617",
                color: "#e5e7eb",
              }}
            />
          </div>

          {/* Amount */}
          <div style={{ marginBottom: "20px", textAlign: "left" }}>
            <label style={{ fontWeight: "600", fontSize: "14px" }}>Amount</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
              style={{
                width: "100%",
                padding: "11px",
                marginTop: "6px",
                borderRadius: "7px",
                border: "1px solid #334155",
                fontSize: "14px",
                background: "#020617",
                color: "#e5e7eb",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading} // disable while predicting
            style={{
              width: "100%",
              padding: "12px",
              border: "none",
              borderRadius: "7px",
              background: "#2563eb",
              color: "white",
              fontSize: "16px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {loading ? "Predicting..." : "Check Fraud"}
          </button>
        </form>

        {/* Progress Bar */}
        {loading && (
          <div
            style={{
              marginTop: "20px",
              height: "8px",
              width: "100%",
              background: "#334155",
              borderRadius: "4px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${progress}%`,
                background: "#2563eb",
                transition: "width 0.3s ease",
              }}
            ></div>
          </div>
        )}

        {/* Result */}
        {result !== null && !loading && (
          <div
            style={{
              marginTop: "22px",
              padding: "12px",
              borderRadius: "7px",
              fontWeight: "bold",
              background: result === 1 ? "#3f1d1d" : "#052e1f",
              color: result === 1 ? "#f87171" : "#34d399",
              border: "1px solid #1f2937",
            }}
          >
            {result === 1 ? "Fraud 🚨" : "Legit ✅"}
          </div>
        )}

        {/* Error */}
        {error && !loading && (
          <div
            style={{
              marginTop: "22px",
              padding: "12px",
              borderRadius: "7px",
              background: "#3f1d1d",
              color: "#f87171",
              fontWeight: "bold",
              border: "1px solid #1f2937",
            }}
          >
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
