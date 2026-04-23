import requests

# 🧠 Agent 1: Location Agent
def location_agent(data):
    # In real-world → GPS / Maps API
    return {
        "lat": data.get("lat", 13.0827),
        "lng": data.get("lng", 80.2707)
    }


# 🏥 Agent 2: Hospital Finder Agent
def hospital_agent(location):
    # In real-world → Google Maps API
    return "Apollo Hospital"


# 🛣️ Agent 3: Route Planner Agent
def route_agent(location, hospital):
    # In real-world → Maps Directions API
    return "Fastest route via Anna Salai"


# 🚑 Agent 4: Ambulance Dispatcher Agent
def ambulance_agent(hospital):
    # In real-world → Ambulance API / Database
    return "Ambulance #12 arriving in 5 mins"


# 📲 Agent 5: Notification Agent
def notification_agent(data):
    # In real-world → SMS / WhatsApp API
    return "Emergency contacts notified"


# 🧠 MASTER AGENT (Planner)
def planner_agent(data):
    print("🚨 Emergency request received")

    # Step 1: Get Location
    location = location_agent(data)
    print("📍 Location:", location)

    # Step 2: Find Hospital
    hospital = hospital_agent(location)
    print("🏥 Hospital:", hospital)

    # Step 3: Plan Route
    route = route_agent(location, hospital)
    print("🛣️ Route:", route)

    # Step 4: Dispatch Ambulance
    ambulance = ambulance_agent(hospital)
    print("🚑 Ambulance:", ambulance)

    # Step 5: Notify Contacts
    notification = notification_agent(data)
    print("📲 Notification:", notification)

    # Step 6: Call n8n Workflow (SAFE)
    try:
        workflow_response = requests.post(
            "http://localhost:5678/webhook/emergency",
            json={
                "location": location,
                "hospital": hospital,
                "emergency": data.get("emergency")
            },
            timeout=5  # 🔥 prevents freezing
        ).json()
    except Exception as e:
        workflow_response = {"error": str(e)}

    print("⚙️ Workflow Response:", workflow_response)

    # Final Response
    return {
        "location": location,
        "hospital": hospital,
        "route": route,
        "ambulance": ambulance,
        "notification": notification,
        "workflow": workflow_response
    }