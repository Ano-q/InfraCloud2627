# ANSIBLE

Ansible-playbooks (Ansible 2.9) voor een Cisco IOS XE-router. Uitvoeren vanuit deze map. Wachtwoord: `export ROUTER_PASS=...`

| Playbook | Wat |
|---|---|
| `06_ios_facts/facts.yaml` | Facts ophalen en opslaan als JSON |
| `07_ios_command/show_interfaces.yaml` | `show ip interface brief` |
| `07_ios_command/save_baseline.yaml` | Running-config opslaan als baseline |
| `07_ios_command/compare_baseline.yaml` | Vergelijken met baseline (`--check --diff`) |
| `08_compliance/compliance.yaml` | Telnet, SSH v2 en password-encryption controleren |
| `09_ios_config/loopback_add.yaml` / `loopback_remove.yaml` | Loopback110 toevoegen / verwijderen |
