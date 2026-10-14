#connect_ios.py ; experiment 1: verbinden met Netmiko en "show ssh" uitvoeren
import os
from getpass import getpass

from netmiko import ConnectHandler

# wachtwoord niet in de code: export ROUTER_PASS=... of het script vraagt erom
password = os.environ.get("ROUTER_PASS") or getpass("Router password: ")

device = {
    "device_type": "cisco_ios",
    "host": "192.168.56.101",
    "username": "cisco",
    "password": password,
    "secret": password,
}

connection = ConnectHandler(**device)
connection.enable()
output = connection.send_command("show ssh")
print(output)
connection.disconnect()
