#!/usr/bin/env python3
#library_books.py ; eval 18 + 19: School Library API - bestaande call uitvoeren (GET books) en boeken toevoegen (POST)
# Aangepast van yroosel/PythonExperiments mixed/add100RandomBooks.py + delete_books.py (slides 20-29):
#  - login/wachtwoord niet in de code: LIBRARY_USER / LIBRARY_PASS of getpass
#  - geen vaste API-key meer: token via /api/v1/loginViaBasic
#  - 5 boeken (id 900-904) i.p.v. 100, daarna controle met GET; --cleanup verwijdert ze weer
# Draait op de DEVASC LABVM (library.demo.local bestaat enkel daar).
import json
import os
import sys
from datetime import datetime
from getpass import getpass

import requests

APIHOST = os.environ.get("LIBRARY_HOST", "http://library.demo.local")
LOGIN = os.environ.get("LIBRARY_USER", "cisco")
PASSWORD = os.environ.get("LIBRARY_PASS") or getpass(f"Library password for {LOGIN}: ")
IDS = range(900, 905)

try:
    from faker import Faker
    fake = Faker()
except ImportError:          # faker niet geinstalleerd -> eenvoudige testdata
    fake = None


def get_auth_token():
    r = requests.post(f"{APIHOST}/api/v1/loginViaBasic", auth=(LOGIN, PASSWORD), timeout=10)
    print("POST /api/v1/loginViaBasic ->", r.status_code)
    if r.status_code != 200:
        sys.exit(f"Auth failed: {r.status_code} {r.text}")
    return r.json()["token"]


def headers(api_key, json_body=False):
    # Content-type enkel bij een body (POST); bij een GET zonder body geeft de API anders 400
    h = {"X-API-Key": api_key}
    if json_body:
        h["Content-type"] = "application/json"
    return h


print(datetime.now())
api_key = get_auth_token()

# eval 18: een beschikbare API-call (zelfde als 'Try it out' in Swagger): GET /api/v1/books
r = requests.get(f"{APIHOST}/api/v1/books", headers=headers(api_key), timeout=10)
books = r.json()
if r.status_code != 200 or not isinstance(books, list):
    sys.exit(f"GET /api/v1/books failed: {r.status_code} {books}")
print(f"GET /api/v1/books -> {r.status_code}, {len(books)} books; first 3:")
print(json.dumps(books[:3], indent=2))

# eval 19: boeken toevoegen
for i in IDS:
    if fake:
        book = {"id": i, "title": fake.catch_phrase(), "author": fake.name(), "isbn": fake.isbn13()}
    else:
        book = {"id": i, "title": f"Infra & Cloud test book {i}", "author": "InfraCloud2627", "isbn": f"978000000{i}"}
    r = requests.post(f"{APIHOST}/api/v1/books", headers=headers(api_key, json_body=True), data=json.dumps(book), timeout=10)
    print(f"POST /api/v1/books id={i} -> {r.status_code}", "added" if r.status_code == 200 else r.text)

# controle: staan ze er nu in?
r = requests.get(f"{APIHOST}/api/v1/books", headers=headers(api_key), timeout=10)
mine = [b for b in r.json() if b.get("id") in IDS]
print(f"\nVerify: {len(mine)}/{len(IDS)} books with id 900-904 found:")
print(json.dumps(mine, indent=2))

if "--cleanup" in sys.argv:
    for i in IDS:
        r = requests.delete(f"{APIHOST}/api/v1/books/{i}", headers=headers(api_key), timeout=10)
        print(f"DELETE /api/v1/books/{i} -> {r.status_code}")
