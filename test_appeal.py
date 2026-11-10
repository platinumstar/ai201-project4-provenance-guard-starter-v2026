import requests

BASE = "http://127.0.0.1:5000"

texts = [
    "As I was walking towards work a bird followed me from one tree to another",
    "I went out during lunch break to the lake to catch a fish, but returned empty handed.",
    "On a hot day, I got in my car and was expecting the ac to cool down, but the ac did not work.",
    "I took my car to the mechanic and they gave me a discount on ac compressor replacement.",
    "I asked a finance executive to explain some calculations to me, and it seemed reasonably easy.",
]

passed = 0
for i, text in enumerate(texts, 1):
    # Submit, keep the content_id
    cid = requests.post(f"{BASE}/submit",
                        json={"text": text, "creator_id": f"eval_appeal_{i}"}).json()["content_id"]

    # Appeal it
    resp = requests.post(f"{BASE}/appeal",
                         json={"content_id": cid, "reasoning": "I wrote this myself."})
    body = resp.json()
    print(i, resp.status_code, body)

    # GET /log must show an appeal entry with this content_id and status under_review
    log = requests.get(f"{BASE}/log").json()["entries"]
    logged = any(e.get("content_id") == cid and e.get("event") == "appeal"
                 and e.get("status") == "under_review" for e in log)
    print("   log entry present:", logged)

    if resp.status_code == 200 and body.get("status") == "under_review" and logged:
        passed += 1

# Unknown content_id: must be 404 and write no appeal entry
before = len([e for e in requests.get(f"{BASE}/log").json()["entries"] if e.get("event") == "appeal"])
bad = requests.post(f"{BASE}/appeal",
                    json={"content_id": "does-not-exist", "reasoning": "typo"})
after = len([e for e in requests.get(f"{BASE}/log").json()["entries"] if e.get("event") == "appeal"])
print("unknown id:", bad.status_code, bad.json(), "| new appeal entries:", after - before)
unknown_ok = bad.status_code == 404 and after == before

print(f"{passed}/5 appeals acknowledged and logged; unknown id refused cleanly: {unknown_ok}")
