# InfraCloud2627

Scripts voor Infrastructure & Cloud (CCNA Automation & DevNet) 2026-2027 – praktijkopdrachten week 1–6 + extra API-opdrachten.
Getest op 24/11/2026 op twee netwerkomgevingen: **CSR1000v 16.9.05** (VirtualBox, 192.168.56.101) en **CML Free 2.10.1 – R1** (IOL, 192.168.210.133).

## Structuur
| Map | Inhoud | Waar uitvoeren |
|---|---|---|
| `SISINFO/` | Week 3 – systeeminformatie: verzamelen, filteren, JSON/CSV/XLSX, samenvoegen, valideren (+ serienummer) | Windows / Linux (`pip install psutil openpyxl`) |
| `GitIntegration/` | Week 3 – Git-commando's | – |
| `PythonExperiment/WEEK2/` | Week 2 – datetime, dict ↔ JSON | overal |
| `PythonExperiment/NETMIKO/` | Week 4–6 – Netmiko eval 1–8 (01 … 05) | Windows `.venv` of Lab VM |
| `PythonExperiment/ANSIBLE/` | Week 4–6 – Ansible eval 9–12 (06 … 09) | DEVASC Lab VM (Ansible 2.9) |
| `PythonExperiment/API/` | Extra – Managing API Calls, School Library, Webex (eval 13–20) | Windows / Lab VM |

Elke map heeft een eigen README met de exacte commando's.

## Snel starten
```bash
# Netmiko op CSR of CML R1
export ROUTER_HOST=192.168.210.133      # PowerShell: $env:ROUTER_HOST = '192.168.210.133'
python PythonExperiment/NETMIKO/03_informatie/device_info.py      # vraagt het routerwachtwoord

# Ansible (Lab VM)
cd PythonExperiment/ANSIBLE && read -s ROUTER_PASS && export ROUTER_PASS
ansible-playbook 08_compliance/compliance.yaml --limit CSR1kv
```

## Veiligheid
Geen wachtwoorden, tokens of API-keys in deze repo: `ROUTER_PASS`, `LIBRARY_PASS`, `WEBEX_TOKEN` of `getpass`.
Uitvoerbestanden (`output/`) staan in `.gitignore` – ze bevatten serienummers, MAC- en IP-adressen.
