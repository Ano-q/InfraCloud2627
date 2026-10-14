#configure_security.py ; experiment 5: basisbeveiliging configureren met Netmiko
import sys
from pathlib import Path

from netmiko import ConnectHandler

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from device import DEVICE

config_commands = [
    "service password-encryption",
    "banner motd #Unauthorized access is prohibited#",
]

connection = ConnectHandler(**DEVICE)
connection.enable()

output = connection.send_config_set(config_commands)
print(output)

print(connection.save_config())

print("\nConfiguration changes:")
print(connection.send_command("show running-config | include service password-encryption|banner motd"))
connection.disconnect()
