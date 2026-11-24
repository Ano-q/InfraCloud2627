#my_ip.py ; eval 13 + 16: publiek IP-adres en land opvragen via een REST API, statuscode + JSON tonen
# Aangepast van yroosel/PythonExperiments mixed/my_ip.py:
#  - TASK uit het origineel: "REPLACE https://api.myip.com by a working API service" -> https://ipinfo.io/json
#  - ontbrekende 'import json' toegevoegd
#  - publiek IP wordt standaard half gemaskeerd (repo is publiek); SHOW_FULL_IP=1 toont alles
import datetime
import json
import os
import sys

import requests

API_URL = "https://ipinfo.io/json"

print(datetime.datetime.now())
r = requests.get(API_URL, timeout=10)
print("Status Code: " + str(r.status_code))                 # eval 16: HTTP-statuscode
print("Content-Type:", r.headers.get("Content-Type"))
if r.status_code != 200:
    print("Error:", r.status_code, r.text, file=sys.stderr)
    sys.exit(1)

data = r.json()                                             # JSON-tekst -> Python dict
ip = data.get("ip")
country = data.get("country")
if ip is None or country is None:
    print("Unexpected response:", data, file=sys.stderr)
    sys.exit(1)

if os.environ.get("SHOW_FULL_IP") != "1":                   # privacy: half maskeren
    ip = ".".join(ip.split(".")[:2] + ["x", "x"])
    for key in ("ip", "hostname", "loc", "postal", "org", "city", "region"):
        if key in data:
            data[key] = "<masked>" if key != "ip" else ip

print("JSON response (dict -> json.dumps):")                # eval 16: JSON-respons
print(json.dumps(data, indent=2))
print("IP Address:", ip)
print("Country:", country)
