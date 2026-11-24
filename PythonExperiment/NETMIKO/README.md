# NETMIKO

Python-scripts (Netmiko) voor een Cisco IOS XE-router via SSH. Wachtwoord: `export ROUTER_PASS=...` (of het script vraagt erom).
Router kiezen: `ROUTER_HOST=192.168.56.101` (CSR, standaard) of `ROUTER_HOST=192.168.210.133` (CML R1).
Op Windows de `.venv` met paramiko 3.5.1 gebruiken: paramiko 5.x kan niet met de oude SSH-algoritmes van CSR 16.9.

| Script | Wat |
|---|---|
| `device.py` | Gedeelde verbindingsparameters |
| `01_verbinding/connect_ios.py` | `show ssh` uitvoeren |
| `02_variabelen/connect_ios_vars.py` | Idem, met variabelen |
| `03_informatie/device_info.py` | Hostname, model, serienummer, versie, interfaces, CDP, routes |
| `04_uitvoer/hostname_to_file.py` | Hostname/model/serienummer met `splitlines()` uit `show version`, opslaan in `output/` als .txt + .json |
| `05_configureren/configure_security.py` | Password-encryption en MOTD-banner instellen |
| `05_configureren/verify_config.py` | Controleert of die configuratie aanwezig is |
