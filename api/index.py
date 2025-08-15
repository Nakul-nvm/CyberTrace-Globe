from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import asyncio
import random

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

# --- NEW: Load our real data from the cache file on startup ---
REAL_ATTACKS_CACHE = []
CACHE_FILE = 'cache.json'
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        REAL_ATTACKS_CACHE = json.load(f)

# This endpoint still serves the cache for the initial load
@app.get("/api/attacks")
def get_attacks():
    return REAL_ATTACKS_CACHE

ATTACK_COLORS = ['#ff4d4d', '#ff944d', '#4d94ff', '#33cc33', '#ffcc00']

@app.websocket("/ws/attacks")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected to WebSocket.")
    # Only run the simulator if we have cached data to work with
    if not REAL_ATTACKS_CACHE:
        print("Cache is empty. Cannot run simulation.")
        return

    try:
        while True:
            # Randomly pick a REAL attacker and target from our cache
            attacker = random.choice(REAL_ATTACKS_CACHE)
            target = random.choice(REAL_ATTACKS_CACHE)
            
            # Ensure attacker and target are not the same
            if attacker['ip'] == target['ip']:
                continue

            new_attack = {
                "startLat": attacker['lat'],
                "startLon": attacker['lon'],
                "endLat": target['lat'],
                "endLon": target['lon'],
                "color": random.choice(ATTACK_COLORS)
            }
            
            await websocket.send_json(new_attack)
            await asyncio.sleep(1) # Send one attack every second
            
    except Exception as e:
        print(f"Client disconnected or error: {e}")