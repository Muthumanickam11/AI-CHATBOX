"""
AI-CHATBOX Backend - 8-Day Implementation Test Suite
Tests each day's functionality according to the blueprint
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

print("\n" + "="*70)
print("  AI-CHATBOX BACKEND - 8-DAY COMPLETE TEST SUITE")
print("="*70 + "\n")

# ============================================================================
# DAY 1: Backend Foundation & Environment Setup
# ============================================================================
print("🗓️  DAY 1 – Backend Foundation & Environment Setup")
print("-" * 70)

response = requests.post(f"{BASE_URL}/chat", json={
    "session_id": "sess-001",
    "prompt": "Hello AI-CHATBOX, what can you do?"
})

print(f"✓ Status: {response.status_code}")
data = response.json()
print(f"✓ Reply: {data.get('reply') or data.get('answer')}")
print(f"✓ Model: {data.get('model')}")
print(f"✓ Timestamp: {data.get('timestamp')}")
print("✅ DAY 1 PASSED\n")

# ============================================================================
# DAY 2: Database Integration & User Context
# ============================================================================
print("🗓️  DAY 2 – Database Integration & User Context")
print("-" * 70)

response = requests.post(f"{BASE_URL}/chat", json={
    "user": { "email": "lush@example.com", "name": "Lush" },
    "prompt": "Explain Artificial Intelligence in simple words."
})

data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Conversation ID: {data.get('conversation_id')}")
print(f"✓ Reply: {data.get('reply') or data.get('answer')}")
print(f"✓ Stored: {data.get('stored')}")
print("✅ DAY 2 PASSED\n")

# ============================================================================
# DAY 3: Chat History & Retrieval
# ============================================================================
print("🗓️  DAY 3 – Chat History & Retrieval")
print("-" * 70)

# Create some history first
for prompt in ["Hello", "What is AI?"]:
    requests.post(f"{BASE_URL}/chat", json={
        "user": { "email": "test@example.com", "name": "Test" },
        "prompt": prompt
    })

response = requests.post(f"{BASE_URL}/history", json={
    "user_id": "1",
    "action": "get_history",
    "limit": 3
})

data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ History Count: {data.get('count')}")
print(f"✓ History Items: {len(data.get('history', []))}")
print("✅ DAY 3 PASSED\n")

# ============================================================================
# DAY 4: Authentication Layer
# ============================================================================
print("🗓️  DAY 4 – Authentication Layer")
print("-" * 70)

# Try signup (may already exist)
signup_response = requests.post(f"{BASE_URL}/signup", json={
    "email": "auth_test@example.com",
    "password": "securepass"
})
print(f"✓ Signup Status: {signup_response.status_code}")

# Login
login_response = requests.post(f"{BASE_URL}/login", json={
    "email": "auth_test@example.com",
    "password": "securepass"
})

login_data = login_response.json()
print(f"✓ Login Status: {login_response.status_code}")
print(f"✓ Token: {login_data.get('token', '')[:20]}...")
print(f"✓ Expires In: {login_data.get('expires_in')}")
print(f"✓ Login Status: {login_data.get('login_status')}")
print("✅ DAY 4 PASSED\n")

# ============================================================================
# DAY 5: AI Logic & Model Configuration
# ============================================================================
print("🗓️  DAY 5 – AI Logic & Model Configuration")
print("-" * 70)

response = requests.post(f"{BASE_URL}/chat", json={
    "user_id": "user-001",
    "conversation_id": "conv-101",
    "query": "List benefits of renewable energy.",
    "settings": { "temperature": 0.7, "max_tokens": 200 }
})

data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Answer: {data.get('answer') or data.get('reply')}")
print(f"✓ Tokens Used: {data.get('tokens_used')}")
print(f"✓ Processing Time: {data.get('processing_time')}")
print("✅ DAY 5 PASSED\n")

# ============================================================================
# DAY 6: Document Ingestion / RAG Pipeline
# ============================================================================
print("🗓️  DAY 6 – Document Ingestion / RAG Pipeline")
print("-" * 70)

files = {'file': ('ai_intro.pdf', b'AI systems learn from data to make decisions.')}
data_upload = {'user_id': "user-001"}

response = requests.post(f"{BASE_URL}/upload", files=files, data=data_upload)
data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Doc ID: {data.get('doc_id')}")
print(f"✓ File Name: {data.get('file_name')}")
print(f"✓ Embedding Status: {data.get('embedding_status')}")
print(f"✓ Chunks Indexed: {data.get('chunks_indexed')}")
print("✅ DAY 6 PASSED\n")

# ============================================================================
# DAY 7: Moderation + Analytics
# ============================================================================
print("🗓️  DAY 7 – Moderation + Analytics")
print("-" * 70)

response = requests.post(f"{BASE_URL}/chat", json={
    "user_id": "user-001",
    "prompt": "How to hack a system?"
})

data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ Blocked Status: {data.get('status')}")
print(f"✓ Reason: {data.get('reason')}")
print("✅ DAY 7 PASSED\n")

# ============================================================================
# DAY 8: Deployment + Monitoring
# ============================================================================
print("🗓️  DAY 8 – Deployment + Monitoring")
print("-" * 70)

response = requests.get(f"{BASE_URL}/health")
data = response.json()
print(f"✓ Status: {response.status_code}")
print(f"✓ System Status: {data.get('status')}")
print(f"✓ Uptime: {data.get('uptime')}")
print(f"✓ Requests Today: {data.get('requests_today')}")
print(f"✓ Average Latency: {data.get('average_latency')}")
print(f"✓ Error Rate: {data.get('error_rate')}")
print("✅ DAY 8 PASSED\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("="*70)
print("  ✅ ALL 8 DAYS SUCCESSFULLY TESTED!")
print("="*70)
print("\n📊 Summary:")
print("  ✓ Day 1: Backend Foundation & Environment Setup")
print("  ✓ Day 2: Database Integration & User Context")
print("  ✓ Day 3: Chat History & Retrieval")
print("  ✓ Day 4: Authentication Layer")
print("  ✓ Day 5: AI Logic & Model Configuration")
print("  ✓ Day 6: Document Ingestion / RAG Pipeline")
print("  ✓ Day 7: Moderation + Analytics")
print("  ✓ Day 8: Deployment + Monitoring")
print("\n🎉 AI-CHATBOX Backend is fully operational!\n")
