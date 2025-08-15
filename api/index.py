from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import os, json, asyncio, random

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load cache
CACHE_FILE = "cache.json"
REAL_ATTACKS_CACHE = []
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        REAL_ATTACKS_CACHE = json.load(f)

# Initial data for the page (points list, not arcs)
@app.get("/api/attacks")
def get_attacks():
    return JSONResponse(REAL_ATTACKS_CACHE)

ATTACK_COLORS = ["#ff4d4d", "#ff944d", "#4d94ff", "#33cc33", "#ffcc00"]

# SSE stream that replaces WebSockets
@app.get("/ws/attacks")
async def sse_attacks(request: Request):
    if not REAL_ATTACKS_CACHE:
        async def empty_stream():
            yield "event: info\ndata: Cache is empty\n\n"
        return StreamingResponse(empty_stream(), media_type="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break

                attacker = random.choice(REAL_ATTACKS_CACHE)
                target = random.choice(REAL_ATTACKS_CACHE)
                if attacker.get("ip") == target.get("ip"):
                    await asyncio.sleep(0)  # yield
                    continue

                new_attack = {
                    "startLat": attacker["lat"],
                    "startLon": attacker["lon"],
                    "endLat": target["lat"],
                    "endLon": target["lon"],
                    "color": random.choice(ATTACK_COLORS)
                }

                yield f"data: {json.dumps(new_attack)}\n\n"
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no"
    })
