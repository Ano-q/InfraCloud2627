# NETMIKO

Python-scripts (Netmiko) voor een Cisco IOS XE-router via SSH. Wachtwoord: `export ROUTER_PASS=...`

| Script | Wat |
|---|---|
| `device.py` | Gedeelde verbindingsparameters |
| `01_verbinding/connect_ios.py` | `show ssh` uitvoeren |
| `02_variabelen/connect_ios_vars.py` | Idem, met variabelen |
| `03_informatie/device_info.py` | Hostname, model, serienummer, versie, interfaces, CDP, routes |
| `05_configureren/configure_security.py` | Password-encryption en MOTD-banner instellen |
| `05_configureren/verify_config.py` | Controleert of die configuratie aanwezig is |
