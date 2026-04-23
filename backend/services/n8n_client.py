import requests

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/emergency"


def trigger_n8n_workflow(data):
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}