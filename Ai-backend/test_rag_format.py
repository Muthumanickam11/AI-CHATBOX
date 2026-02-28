"""
Test to verify RAG response format matches Day 6 blueprint
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

print("\n" + "="*70)
print("  Testing RAG Response Format (Day 6)")
print("="*70 + "\n")

# Test with a query that triggers RAG
response = requests.post(f"{BASE_URL}/chat", json={
    "prompt": "According to my uploaded document, what is AI?"
})

data = response.json()
print("Response:")
print(json.dumps(data, indent=2))

# Verify RAG fields
if "sources" in data and data["sources"]:
    print("\n✅ RAG sources field present")
    print(f"   Sources: {data['sources']}")
else:
    print("\n⚠️  No sources in response (RAG not triggered)")

# Verify answer field (Day 6 uses 'answer' instead of 'reply')
if "answer" in data:
    print(f"✅ Answer field present: {data['answer'][:50]}...")
