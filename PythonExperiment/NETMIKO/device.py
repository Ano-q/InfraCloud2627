#device.py ; gedeelde verbindingsparameters voor experiment 3 en 5
# Pas deze waarden aan naar jouw router (CSR1kv in de DEVASC-labo-omgeving).
import os
from getpass import getpass

v_device_type = "cisco_ios"
v_host = "192.168.56.101"
v_ssh_port = 22
v_username = "cisco"
# wachtwoord niet in de code: export ROUTER_PASS=... of het script vraagt erom
v_password = os.environ.get("ROUTER_PASS") or getpass("Router password: ")
v_secret = v_password

DEVICE = {
    "device_type": v_device_type,
    "host": v_host,
    "port": v_ssh_port,
    "username": v_username,
    "password": v_password,
    "secret": v_secret,
}
