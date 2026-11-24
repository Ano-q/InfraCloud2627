#hostname_to_file.py ; experiment 4: hostname uit "show version" halen (splitlines) en opslaan in tekst + json
# Aangepast van yroosel/PythonExperiments netmiko/netmiko_gather_information_splitlines.py:
#  - geen wachtwoorden in de code (device.py: ROUTER_PASS of getpass)
#  - werkt op CSR en CML R1 (ROUTER_HOST)
#  - resultaat wordt bewaard in output/<hostname>_info.txt en .json
import json
import sys
from datetime import datetime
from pathlib import Path

from netmiko import ConnectHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from device import DEVICE

connection = ConnectHandler(**DEVICE)
connection.enable()
output = connection.send_command("show version")
interfaces = connection.send_command("show ip interface brief")
connection.disconnect()

# tekstverwerking met splitlines(): elke regel apart bekijken
hostname = model = serial = version = "Unknown"
for line in output.splitlines():
    if "uptime is" in line:
        hostname = line.split()[0]                 # eerste woord: "R1 uptime is ..."
    if line.lower().startswith("cisco ") and "(" in line and "processor" in line:
        model = line.split()[1]                    # "cisco CSR1000V (VXE) processor ..."
    if "Processor board ID" in line:
        serial = line.split()[-1]                  # laatste woord
    if version == "Unknown" and "Version" in line and ("IOS" in line or "Cisco" in line):
        version = line.split("Version")[1].split(",")[0].strip()

info = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "host": DEVICE["host"],
    "hostname": hostname,
    "model": model,
    "serial": serial,
    "version": version,
}

outdir = Path(__file__).resolve().parent.parent / "output"
outdir.mkdir(exist_ok=True)
txt = outdir / f"{hostname}_info.txt"
txt.write_text(
    "\n".join(f"{k}: {v}" for k, v in info.items()) + "\n\n" + interfaces + "\n",
    encoding="utf-8",
)
(outdir / f"{hostname}_info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")

print(json.dumps(info, indent=2))
print(f"\nSaved: {txt.name} and {hostname}_info.json in {outdir}")
