from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import math
import requests

app = FastAPI()

# ✅ Allow frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon (restrict later in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏥 Dummy hospital database
HOSPITALS = [
    {"name": "Apollo Hospital", "lat": 13.0843, "lng": 80.2705},
    {"name": "MIOT International", "lat": 13.0215, "lng": 80.1850},
    {"name": "Fortis Malar", "lat": 13.0067, "lng": 80.2573},
]

# 📏 Distance calculator (Haversine formula)
def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# 🚨 Emergency endpoint
@app.post("/emergency")
def handle_emergency(data: dict):
    try:
        # 📍 Extract location
        lat = data["location"]["lat"]
        lng = data["location"]["lng"]
        emergency_type = data.get("emergency", "general")

        print(f"🚨 Emergency received: {data}")

        # 🏥 Find nearest hospital
        nearest = None
        min_dist = float("inf")

        for hospital in HOSPITALS:
            dist = calculate_distance(lat, lng, hospital["lat"], hospital["lng"])
            if dist < min_dist:
                min_dist = dist
                nearest = hospital

        # ⚡ Priority logic (AI simulation)
        if emergency_type in ["heart", "accident"]:
            priority = "HIGH"
            eta = "5 mins"
            ambulance = "Advanced Life Support"
        else:
            priority = "MEDIUM"
            eta = "10 mins"
            ambulance = "Basic Ambulance"

        # 🌍 Map link
        map_link = f"https://www.google.com/maps?q={lat},{lng}"

        # 📦 Final response
        response_data = {
            "hospital": nearest["name"],
            "ambulance": ambulance,
            "priority": priority,
            "eta": eta,
            "distance_km": round(min_dist, 2),
            "location": {
                "lat": lat,
                "lng": lng
            },
            "map": map_link
        }

        # 🔥 SEND DATA TO N8N (IMPORTANT FIX)
        n8n_payload = {
            "emergency": emergency_type,
            "hospital": nearest["name"],
            "priority": priority,
            "eta": eta,
            "distance_km": round(min_dist, 2),
            "location": {
                "lat": lat,
                "lng": lng
            }
        }

        try:
            requests.post(
                "http://localhost:5678/webhook/emergency",
                json=n8n_payload,
                timeout=5
            )
            print("✅ Sent to n8n successfully")
        except Exception as e:
            print("❌ n8n not reachable:", str(e))

        return {"response": response_data}

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}


# 🏠 Health check
@app.get("/")
def home():
    return {"message": "LifeLine AI Backend Running 🚑"}