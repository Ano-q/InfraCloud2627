# Git-integratie

Deze map documenteert de commando's die gebruikt zijn om deze repository aan te maken en op GitHub te publiceren.
Persoonlijke gegevens zijn vervangen door placeholders zoals `<jouw-naam>`.

## Gebruikte commando's

```bash
git config --global user.name "<jouw-naam>"
git config --global user.email "<jouw-email>"
mkdir InfraCloud2627
cd InfraCloud2627
echo "# InfraCloud2627" > README.md
git init
git status
git add README.md
git commit -m "Created README.md for InfraCloud2627"
git branch -M main
git remote add origin https://github.com/<github-gebruikersnaam>/InfraCloud2627.git
git push -u origin main
```

## Wat elk commando doet

| Commando | Doel |
|---|---|
| `git config --global user.name` | Stelt de auteursnaam in die aan elke commit op deze computer gekoppeld wordt. |
| `git config --global user.email` | Stelt het e-mailadres van de auteur in. Dit moet overeenkomen met een e-mailadres van het GitHub-account. |
| `mkdir InfraCloud2627` | Maakt de projectmap aan. |
| `cd InfraCloud2627` | Gaat naar de projectmap. Alle Git-commando's moeten vanuit deze map uitgevoerd worden. |
| `echo "# InfraCloud2627" > README.md` | Maakt een README-bestand aan met een Markdown-titel. |
| `git init` | Maakt van de map een Git-repository door de verborgen map `.git` aan te maken. |
| `git status` | Toont welke bestanden nieuw, gewijzigd of gestaged zijn. |
| `git add README.md` | Staget het bestand, zodat het in de volgende commit wordt opgenomen. |
| `git commit -m "..."` | Slaat lokaal een momentopname van de gestagede bestanden op, met een beschrijving. |
| `git branch -M main` | Hernoemt de standaardbranch naar `main`. |
| `git remote add origin <url>` | Koppelt de lokale repository aan de GitHub-repository onder de naam `origin`. |
| `git push -u origin main` | Uploadt de commits naar GitHub. `-u` koppelt de lokale en externe `main`-branch, zodat later `git push` volstaat. |

## Dagelijkse werkwijze

```bash
git pull                 # laatste versie van GitHub ophalen
git status               # controleren wat er gewijzigd is
git add <bestanden>      # wijzigingen stagen
git commit -m "bericht"  # momentopname opslaan
git push                 # uploaden naar GitHub
```

## Authenticatie

GitHub aanvaardt geen accountwachtwoorden voor Git via HTTPS. Authenticatie gebeurt via
Git Credential Manager (aanmelden in de browser) of een Personal Access Token dat ingegeven wordt wanneer Git om een wachtwoord vraagt.
Tokens mogen nooit in deze repository opgeslagen worden.

## Opmerking

De GitHub-repository moet eerst op github.com aangemaakt worden (leeg, zonder README) voor de eerste push.
Anders mislukt de push met de fout "Repository not found".
