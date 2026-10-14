#connect_ios_vars.py ; experiment 2: zelfde script, maar met variabelen
import os
from getpass import getpass

from netmiko import ConnectHandler

v_device_type = "cisco_ios"
v_host = "192.168.56.101"
v_ssh_port = 22
v_username = "cisco"
# wachtwoord niet in de code: export ROUTER_PASS=... of het script vraagt erom
v_password = os.environ.get("ROUTER_PASS") or getpass("Router password: ")
v_secret = v_password

device = {
    "device_type": v_device_type,
    "host": v_host,
    "port": v_ssh_port,
    "username": v_username,
    "password": v_password,
    "secret": v_secret,
}

connection = ConnectHandler(**device)
connection.enable()
output = connection.send_command("show ssh")
print(output)
connection.disconnect()
