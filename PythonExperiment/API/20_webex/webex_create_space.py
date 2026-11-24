#webex_create_space.py ; eval 20: met de Webex REST API een Space aanmaken (Python)
# Aangepast van yroosel/PythonExperiments webex/webex_people_me.py + testing_webex_script.py (slides 30-32):
#  - token NOOIT in de code: WEBEX_TOKEN env var of verborgen prompt (token: developer.webex.com, 12 uur geldig)
#  - stap 1: GET /people/me (token testen), stap 2: POST /rooms (space maken), stap 3: GET /rooms (controle)
#  - GEEN leden toevoegen: dat stuurt echte uitnodigingen naar andere mensen
#  - persoonlijke gegevens worden gemaskeerd in de uitvoer; --delete verwijdert de space weer
import json
import os
import sys
from datetime import datetime
from getpass import getpass

import requests

API = "https://webexapis.com/v1"
token = os.environ.get("WEBEX_TOKEN") or getpass("Webex personal access token (hidden): ")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
title = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "InfraCloud2627 - API test space"


def mask(value):
    return value[:2] + "***" if isinstance(value, str) and value else value


print(datetime.now())
print("---------- 1. GET /people/me ----------")
r = requests.get(f"{API}/people/me", headers=headers, timeout=10)
print("Status code:", r.status_code)
if not r.ok:
    sys.exit(f"Token not valid: {r.status_code} {r.text[:200]}")
me = r.json()
print("Name:", mask(me.get("displayName")), "| type:", me.get("type"), "| status:", me.get("status"))

print("\n---------- 2. POST /rooms ----------")
r = requests.post(f"{API}/rooms", headers=headers, json={"title": title}, timeout=10)
print("Status code:", r.status_code)
if not r.ok:
    sys.exit(f"Create failed: {r.status_code} {r.text[:200]}")
room = r.json()
print(json.dumps({k: room.get(k) for k in ("title", "type", "isLocked", "created")}, indent=2))
print("Room id:", room["id"][:12] + "...")

print("\n---------- 3. GET /rooms (verify) ----------")
r = requests.get(f"{API}/rooms", headers=headers, params={"max": 50, "sortBy": "created"}, timeout=10)
found = [x for x in r.json().get("items", []) if x["id"] == room["id"]]
print("Status code:", r.status_code, "| new space found in list:", bool(found))

if "--delete" in sys.argv:
    r = requests.delete(f"{API}/rooms/{room['id']}", headers=headers, timeout=10)
    print("\nDELETE /rooms/<id> ->", r.status_code, "(204 = deleted)")
