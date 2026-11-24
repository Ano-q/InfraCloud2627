#geopy_folium_location.py ; eval 14 + 15: coördinaten van een stad opzoeken (Geopy) en een kaart maken (Folium)
# Aangepast van yroosel/PythonExperiments mixed/geopy-geocoders_location.py:
#  - stad als argument (standaard "Leuven, Belgium"), eigen user_agent
#  - kaart krijgt een marker en wordt in output/ bewaard en (optioneel) in de browser geopend
# Gebruik: python geopy_folium_location.py "Gent, Belgium" [--open]
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import folium
from geopy.geocoders import Nominatim

city_country = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "Leuven, Belgium"

print(datetime.now())
geolocator = Nominatim(user_agent="infracloud2627-student-lab")   # Nominatim vereist een user_agent
location = geolocator.geocode(city_country, timeout=10)
if location is None:
    sys.exit(f"Location not found: {city_country}")

print("Address :", location.address)
print("Lat/Lon :", (location.latitude, location.longitude))

m = folium.Map(location=[location.latitude, location.longitude], tiles="OpenStreetMap", zoom_start=12)
folium.Marker([location.latitude, location.longitude], popup=city_country).add_to(m)

out = Path(__file__).resolve().parent / "output"
out.mkdir(exist_ok=True)
html = out / ("map_" + city_country.split(",")[0].strip().lower().replace(" ", "_") + ".html")
m.save(str(html))
print("Map saved:", html)
if "--open" in sys.argv:
    webbrowser.open(html.as_uri())
