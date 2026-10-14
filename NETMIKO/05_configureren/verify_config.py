#verify_config.py ; experiment 5: controleren of de configuratie is toegepast
import sys
from pathlib import Path

from netmiko import ConnectHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from device import DEVICE

# IOS toont het banner-scheidingsteken als ^C, dus enkel de tekst zelf controleren
checks = {
    "service password-encryption": "service password-encryption",
    "banner motd": "Unauthorized access is prohibited",
}

connection = ConnectHandler(**DEVICE)
connection.enable()
running_config = connection.send_command("show running-config")
connection.disconnect()

all_ok = True
for name, expected in checks.items():
    ok = expected in running_config
    all_ok = all_ok and ok
    print(f"[{'OK' if ok else 'NOK'}] {name}")

sys.exit(0 if all_ok else 1)
