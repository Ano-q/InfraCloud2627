# 02 - Filteren

| Script | Doel |
|---|---|
| `system_details.py` | Voegt computermodel, leesbare processornaam en serienummer toe (via PowerShell, `/sys` of `sysctl`, afhankelijk van het besturingssysteem). |
| `primary_interface.py` | Zoekt de interface waarlangs het internetverkeer loopt. Reserve: de actieve interface met een bruikbaar IPv4-adres en het meeste ontvangen verkeer. |
| `filter_sysinfo.py` | Herleidt alles tot één platte rij van 13 kolommen (`KOLOMMEN`). Gebruikt de systeempartitie, groottes in GB en MAC-adressen in hoofdletters met dubbele punten. |
