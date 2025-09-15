import { useEffect, useState } from "react";

const API_URL = "https://stqc-decoder.onrender.com"; // <- podmień na swój adres Render

function App() {
  const [logs, setLogs] = useState([]);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(API_URL.replace("http", "ws") + "/ws");
    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data);
      setLogs((prev) => [data, ...prev]);
    };

    fetch(API_URL + "/events")
      .then((r) => r.json())
      .then(setEvents);
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Dekoder STQC</h1>

      <h2>Na żywo</h2>
      <ul>
        {logs.map((e, i) => (
          <li key={i}>{e.timestamp} → {e.code} = {e.description}</li>
        ))}
      </ul>

      <h2>Historia</h2>
      <ul>
        {events.map((e, i) => (
          <li key={i}>{e.timestamp} → {e.code} = {e.description}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
