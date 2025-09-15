from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests, datetime, asyncio
from pathlib import Path

from .database import init_db, save_event, get_events

app = FastAPI()
init_db()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # w produkcji ogranicz np. do GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- konfiguracja Discord webhook ---
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/TU_WKLEJ_WEBHOOK"

CODE_MAP = {
    "1234": "Alarm pożarowy",
    "5678": "Test systemu"
}

@app.post("/event")
async def receive_event(request: Request):
    body = await request.json()
    seq = body.get("code")
    desc = body.get("description") or CODE_MAP.get(seq, "Nieznana sekwencja")
    ts = datetime.datetime.now().isoformat()

    save_event(ts, seq, desc)

    try:
        requests.post(DISCORD_WEBHOOK, json={
            "content": f"🚨 [{ts}] {seq} → {desc}"
        })
    except Exception as e:
        print("❌ Błąd wysyłania do Discord:", e)

    return {"status": "ok", "timestamp": ts, "code": seq, "description": desc}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        events = get_events()
        if events:
            await ws.send_json(events[0])
        await asyncio.sleep(5)

@app.get("/events")
def api_events():
    return get_events()

@app.get("/")
def index():
    frontend_index = Path(__file__).resolve().parent.parent / "frontend" / "build" / "index.html"
    return FileResponse(frontend_index)
