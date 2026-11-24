#dict_json_conversion.py ; week 2 opdracht 8: Python dict <-> JSON
# Aangepast van yroosel/PythonExperiments json/json_conversion.py + DOCU Sep30-2026 "Voorbeeld dict en json"
#  - JSON-tekst (str) -> dict met json.loads, dict -> JSON-tekst met json.dumps
#  - filteren kan enkel in een dict/list, niet in een string
import datetime
import json

print(datetime.datetime.now())

# JSON zoals een API (RESTCONF ietf-interfaces) het terugstuurt: dit is gewoon TEKST
if_json = """
{"ietf-interfaces:interfaces": {"interface": [
  {"name": "GigabitEthernet1", "description": "VBox", "enabled": true,
   "ietf-ip:ipv4": {"address": [{"ip": "192.168.56.101", "netmask": "255.255.255.0"}]}},
  {"name": "Loopback9", "description": "999", "enabled": true,
   "ietf-ip:ipv4": {"address": [{"ip": "10.9.9.9", "netmask": "255.255.255.0"},
                                {"ip": "172.29.0.9", "netmask": "255.255.255.0"}]}}
]}}
"""
print("1. type of if_json        :", type(if_json))          # str

if_dict = json.loads(if_json)                                 # loads: str -> dict (boomstructuur)
print("2. after json.loads       :", type(if_dict))           # dict

print("3. top-level keys         :", list(if_dict.keys()))
for intf in if_dict["ietf-interfaces:interfaces"]["interface"]:   # list -> index/loop, dict -> keys
    ips = [a["ip"] for a in intf["ietf-ip:ipv4"]["address"]]
    print(f"   {intf['name']:<17} enabled={intf['enabled']!s:<5} ips={ips}")

back = json.dumps(if_dict, indent=2)                          # dumps: dict -> str (om te versturen/bewaren)
print("4. after json.dumps       :", type(back))
print("5. JSON true -> Python True:", if_dict["ietf-interfaces:interfaces"]["interface"][0]["enabled"] is True)
print(back[:200] + " ...")
