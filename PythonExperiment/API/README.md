# API – Managing API Calls (eval 13–20)

Aangepast van [yroosel/PythonExperiments](https://github.com/yroosel/PythonExperiments) (mixed/, webex/) en [IaCExperiments](https://github.com/yroosel/IaCExperiments) (scripts/).
Geen wachtwoorden of tokens in de code: alles via omgevingsvariabelen of een verborgen prompt.

| Map / script | Eval | Uitvoeren | Geheimen |
|---|---|---|---|
| `13_16_my_ip/my_ip.py` | 13 + 16 | `python my_ip.py` | – (publiek IP half gemaskeerd, `SHOW_FULL_IP=1` toont alles) |
| `14_15_geopy_folium/geopy_folium_location.py` | 14 + 15 | `python geopy_folium_location.py "Gent, Belgium" --open` | – (kaart in `output/`) |
| `17_curl/curl_get.sh` | 17 | `bash curl_get.sh [URL]` | – |
| `18_19_school_library/library_books.py` | 18 + 19 | op de DEVASC Lab VM: `python3 library_books.py [--cleanup]` | `LIBRARY_PASS` of prompt |
| `20_webex/webex_create_space.py` | 20 | `python webex_create_space.py ["Titel"] [--delete]` | `WEBEX_TOKEN` of verborgen prompt |

Vereisten: `pip install requests geopy folium` (+ `faker` op de Lab VM voor 18–19).
