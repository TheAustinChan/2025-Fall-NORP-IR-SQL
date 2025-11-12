import requests
import json

BASE_API = "http://130.207.3.31/norpmetabase/api"  # note the /norpmetabase/api
USERNAME = "testuser@gatech.edu"
PASSWORD = "GPJqCK9amq7s2d"

def get_session_id():
    r = requests.post(
        f"{BASE_API}/session",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["id"]

def api_get(path, session_id=None, api_key=None, **params):
    headers = {}
    if api_key:
        headers["X-API-Key"] = api_key
    elif session_id:
        headers["X-Metabase-Session"] = session_id
    r = requests.get(f"{BASE_API}{path}", headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

# --- usage with session token ---
sid = get_session_id()

# Sanity check: who am I?
me = api_get("/user/current", session_id=sid)
print("Logged in as:", me.get("email"), "| ID:", me.get("id"))

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

headers["X-Metabase-Session"] = sid

url = "http://130.207.3.31/norpmetabase/api/dataset"

payload = {
    "database": 2,
    "type": "query",
    "query": {
        "source-table": 46,
        "filter": ["=", ["field", 83, None], "Amal Heights"]
    },
    "parameters": []
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except ValueError:
    print("Response Text:", response.text)