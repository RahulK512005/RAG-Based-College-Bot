import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_suite():
    print("\n=======================================================")
    print("  RUNNING BACKEND API ENDPOINT TEST SUITE")
    print("=======================================================\n")

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    assert res.json() == {"status": "ok"}
    print("[PASS] GET /health -> 200 OK")

    # 2. Student Signup & Login
    signup_payload = {
        "name": "Test Student",
        "email": "teststudent@college.edu",
        "password": "Password@123",
        "confirm_password": "Password@123"
    }
    signup_res = client.post("/api/auth/signup", json=signup_payload)
    if signup_res.status_code == 400 and "already exists" in signup_res.text:
        print("[INFO] Test student already exists, testing login...")
    else:
        assert signup_res.status_code == 200, f"Signup failed: {signup_res.text}"
        assert signup_res.json()["user"]["role"] == "student"
        print("[PASS] POST /api/auth/signup -> 200 OK (Enforced student role)")

    login_res = client.post("/api/auth/login", json={
        "email": "teststudent@college.edu",
        "password": "Password@123"
    })
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    student_token = login_res.json()["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    print("[PASS] POST /api/auth/login -> 200 OK")

    # 3. GET /api/auth/me
    me_res = client.get("/api/auth/me", headers=student_headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "teststudent@college.edu"
    print("[PASS] GET /api/auth/me -> 200 OK")

    # 4. Admin Auth
    admin_login_res = client.post("/api/auth/login", json={
        "email": "admin@college.edu",
        "password": "Admin@123456"
    })
    assert admin_login_res.status_code == 200
    admin_token = admin_login_res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("[PASS] POST /api/auth/login (Admin) -> 200 OK")

    # 5. Role Authorization Enforcement: Student cannot access Admin endpoints
    doc_access_res = client.get("/api/documents", headers=student_headers)
    assert doc_access_res.status_code == 403, f"Expected 403 for student accessing /api/documents, got {doc_access_res.status_code}"
    print("[PASS] GET /api/documents (Student Access Blocked) -> 403 Forbidden")

    # 6. Admin can access /api/documents and /api/analytics/stats
    admin_docs_res = client.get("/api/documents", headers=admin_headers)
    assert admin_docs_res.status_code == 200
    assert "documents" in admin_docs_res.json()
    print(f"[PASS] GET /api/documents (Admin Access) -> 200 OK (Found {len(admin_docs_res.json()['documents'])} documents)")

    stats_res = client.get("/api/analytics/stats", headers=admin_headers)
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["ready_documents"] >= 1
    print(f"[PASS] GET /api/analytics/stats -> 200 OK (Ready docs: {stats['ready_documents']}, Chunks: {stats['total_chunks']})")

    # 7. Student Chat RAG Question
    chat_payload = {
        "question": "What is the tuition fee for B.Tech CSE?"
    }
    chat_res = client.post("/api/chat", json=chat_payload, headers=student_headers)
    assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
    chat_data = chat_res.json()
    assert len(chat_data["sources"]) > 0, "Expected sources in response"
    assert chat_data["is_unknown"] is False
    session_id = chat_data["session_id"]
    message_id = chat_data["message_id"]
    print(f"[PASS] POST /api/chat (Grounded Question) -> 200 OK (Sources: {len(chat_data['sources'])})")

    # 8. Student Unknown Question (Zero-hallucination refusal)
    unknown_payload = {
        "question": "What is the recipe for chocolate chip pancakes in the physics lab?",
        "session_id": session_id
    }
    unknown_res = client.post("/api/chat", json=unknown_payload, headers=student_headers)
    assert unknown_res.status_code == 200
    unknown_data = unknown_res.json()
    assert unknown_data["is_unknown"] is True
    assert "couldn't find reliable information" in unknown_data["answer"].lower()
    print("[PASS] POST /api/chat (Unknown Question Refusal) -> 200 OK (Refused safely without hallucinating)")

    # 9. List and Get Chat Session History
    chats_res = client.get("/api/chats", headers=student_headers)
    assert chats_res.status_code == 200
    assert len(chats_res.json()) >= 1
    print(f"[PASS] GET /api/chats -> 200 OK ({len(chats_res.json())} sessions found)")

    # 10. Message Feedback
    fb_res = client.post(f"/api/messages/{message_id}/feedback", json={"rating": 1, "comment": "Accurate fee information!"}, headers=student_headers)
    assert fb_res.status_code == 200
    print("[PASS] POST /api/messages/{id}/feedback -> 200 OK")

    print("\nALL BACKEND API TESTS COMPLETED AND VERIFIED SUCCESSFULLY!\n")

if __name__ == "__main__":
    test_api_suite()
