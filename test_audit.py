import requests

BASE = "http://127.0.0.1:5000"

texts = [
    f"Test submission number {i}: I walked to the store and bought some apples."
    for i in range(1, 21)
]

ids = []
for i, t in enumerate(texts, 1):
    r = requests.post(f"{BASE}/submit", json={"text": t, "creator_id": f"eval_audit_{i}"})
    body = r.json()
    print(i, r.status_code, body.get("content_id"), body.get("guess"))
    if r.status_code == 200:
        ids.append(body["content_id"])

log = requests.get(f"{BASE}/log").json()["entries"]
logged = {e.get("content_id") for e in log if e.get("status") == "decided"}
found = sum(1 for cid in ids if cid in logged)
print(f"{found}/20 decisions found in the audit log")
