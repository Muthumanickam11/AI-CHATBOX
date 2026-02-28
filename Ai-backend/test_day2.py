import requests
import json

url = "http://127.0.0.1:8000/api/v1/chat"
payload = {
    "user": { "email": "lush@example.com", "name": "Lush" },
    "prompt": "Explain Artificial Intelligence in simple words."
}

try:
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
