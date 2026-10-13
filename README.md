# My Festival API — M10 (CSC Rahti)

🇫🇮 [Suomeksi](#suomeksi) · 🇬🇧 [In English](#in-english)

---

## Suomeksi

Tämä kansio on M10-tehtävän lähtöpohja. Lisää siihen oma `myfestival.db`, toteuta TODO-kohdat
tiedostossa `app.py` ja julkaise sovellus CSC:n Rahti-konttipilveen.

| Tiedosto | Mitä se tekee |
|---|---|
| `app.py` | Flask-sovellus. `GET /api/artists`, `/api/days` ja `/api/stages` ovat valmiit; muut reitit ovat TODO. |
| `myfestival.db` | Festivaalikanta. Korvaa omalla My Festival -kannallasi. |
| `requirements.txt` | Python-riippuvuudet (Flask, gunicorn). |
| `Dockerfile` | Ohje, jolla Rahti rakentaa kontin. Ei tarvitse muokata. |
| `test_endpoints.py` | Tarkistin (20 tarkistusta). Hakee tunnisteet sinun kannastasi, lisää testirivin ja poistaa sen. Kaiken pitää olla vihreää. |
| `ENDPOINTS.md` | Endpoint-dokumentin pohja. Täytä ja palauta Moodleen. |
| `deploy_rahti.sh` | Valinnainen: julkaisu komentoriviltä web-konsolin sijaan. |

### 1. Aja paikallisesti
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                      # → http://localhost:8080/api/artists
python test_endpoints.py http://localhost:8080   # toisessa terminaalissa
```
Windows PowerShell: `curl` on eri ohjelma — käytä `curl.exe`:ä, selainta tai tarkistinta.
Jos `python`-komentoa ei löydy, kokeile `python3` (Windowsissa myös `py`).
`localhost` on vain oman koneesi osoite. Lähtöpohjan TODO-reitit palauttavat 501, joten 20/20 on tavoite vasta toteutuksen jälkeen.

### 2. Vie GitHubiin
Luo GitHubiin **julkinen** repo (esim. `my-festival-api`). Voit tehdä ensimmäisen viennin selaimessa:
valitse uuden repon luomisessa README, avaa repo, paina **Add file → Upload files**, valitse tämän
kansion tiedostot ja paina **Commit changes**. Erillistä `git push` -komentoa ei silloin tarvita.
Vaihtoehtoisesti tee commit omalla koneellasi ja pushaa se Gitiä tai GitHub Desktopia käyttäen.
Tiedostojen pitää olla repon juuressa (Dockerfile ylimmällä tasolla), ei `starter/`-alikansiossa.
Tarkista ennen latausta, ettei mukana ole `.venv`-kansiota, salasanoja, tokeneita tai henkilötietoja.

### 3. Julkaise Rahtiin (web-konsoli)
1. Kirjaudu <https://console.rahti.csc.fi> (CSC-tunnus tai Haka).
2. **Create Project** → *Name:* `festival-<csc-tunnuksesi>` → *Description:* `csc_project: 2021201`
   (kurssin CSC-projektin numero, tarkista Moodlesta).
3. Avaa projektissa **Add** → **Import from Git** → liitä repon URL.
   Rahti tunnistaa Dockerfilen; jos saat ilmoituksen *Multiple import strategies detected*,
   käytä suositeltua strategiaa **Dockerfile**.
4. *Name:* `festival-api`. Varmista, että **Create a route** on valittuna.
   Avaa *Show advanced Routing options* → valitse **Secure Route**, *TLS termination: Edge*,
   *Insecure traffic: Redirect*.
5. *Target port:* **8080**. Avaa **Resource limits** ja aseta:
   CPU request **50** millicores, CPU limit **250** millicores,
   Memory request **128 Mi**, Memory limit **256 Mi** (kurssin kiintiö on yhteinen!).
6. **Create**. Rakentuminen kestää muutaman minuutin. *Topology*-näkymässä nuolikuvake avaa julkisen
   osoitteen, joka päättyy `rahtiapp.fi` (usein muodossa `...2.rahtiapp.fi`). Kopioi se sieltä.
7. Aja tarkistin julkista osoitetta vasten:
   `python test_endpoints.py https://<osoitteesi>`

**Muutokset koodiin:** pushaa GitHubiin ja paina Rahdissa *Builds → festival-api → Start build*
(tai lisää GitHub-webhook, jolloin build käynnistyy automaattisesti).

### Hyvä tietää
- Rahti ajaa kontin satunnaisella käyttäjä-id:llä. Dockerfile antaa sille kirjoitusoikeuden kantaan.
- SQLite kulkee imagessa: POST-lisäykset **katoavat**, kun uusi Pod tai build ottaa käyttöön
  imagen mukana pakatun kannan. Säilytä alkuperäinen kanta myös omalla koneellasi.
  Tämä on tehtävässä hyväksyttyä.
- Kaikki saman CSC-projektin jäsenet näkevät toistensa Rahti-projektit. Älä muuta muiden projekteja.
- Kurssin jälkeen poista projektisi: *Project → Actions → Delete project*.

---

## In English

This folder is the M10 starter. Add your own `myfestival.db`, implement the TODOs in `app.py`
and deploy the app to CSC's Rahti container cloud.

| File | What it does |
|---|---|
| `app.py` | Flask app. `GET /api/artists`, `/api/days` and `/api/stages` are ready; the other routes are TODO. |
| `myfestival.db` | Festival database. Replace it with your own My Festival database. |
| `requirements.txt` | Python dependencies (Flask, gunicorn). |
| `Dockerfile` | Instructions Rahti uses to build the container. No edits needed. |
| `test_endpoints.py` | The checker (20 checks). Reads ids from your database, inserts a test row and deletes it. Everything must be green. |
| `ENDPOINTS.md` | Endpoint document template. Fill in and submit to Moodle. |
| `deploy_rahti.sh` | Optional: deploy from the command line instead of the web console. |

### 1. Run locally
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                      # → http://localhost:8080/api/artists
python test_endpoints.py http://localhost:8080   # in a second terminal
```
Windows PowerShell: `curl` is a different program — use `curl.exe`, a browser or the checker.
If `python` is not found, try `python3` (or `py` on Windows).
`localhost` only points to your own computer. Starter TODO routes return 501, so 20/20 is the goal after implementation.

### 2. Push to GitHub
Create a **public** GitHub repo (e.g. `my-festival-api`). You can make the first upload in a browser:
add a README when creating the repo, open it, choose **Add file → Upload files**, select this folder's
files and click **Commit changes**. No separate `git push` command is needed in this path.
Alternatively, commit on your computer and push with Git or GitHub Desktop.
The files must be at the repo root (Dockerfile at the top level), not inside an extra `starter/` folder.
Before uploading, check that you did not include `.venv`, passwords, tokens or personal data.

### 3. Deploy to Rahti (web console)
1. Log in at <https://console.rahti.csc.fi> (CSC account or Haka).
2. **Create Project** → *Name:* `festival-<your-csc-username>` → *Description:* `csc_project: 2021201`
   (the course CSC project number; check Moodle).
3. In the project, open **Add** → **Import from Git** → paste the repo URL.
   Rahti detects the Dockerfile; if you see *Multiple import strategies detected*,
   use the recommended **Dockerfile** strategy.
4. *Name:* `festival-api`. Make sure **Create a route** is ticked.
   Open *Show advanced Routing options* → tick **Secure Route**, *TLS termination: Edge*,
   *Insecure traffic: Redirect*.
5. *Target port:* **8080**. Open **Resource limits** and set:
   CPU request **50** millicores, CPU limit **250** millicores,
   Memory request **128 Mi**, Memory limit **256 Mi** (the course quota is shared!).
6. **Create**. The build takes a few minutes. In the *Topology* view the arrow icon opens the public
   URL, which ends in `rahtiapp.fi` (often in the form `...2.rahtiapp.fi`). Copy it from there.
7. Run the checker against the public URL:
   `python test_endpoints.py https://<your-url>`

**Code changes:** push to GitHub and in Rahti click *Builds → festival-api → Start build*
(or add a GitHub webhook so builds start automatically).

### Good to know
- Rahti runs the container with a random user id. The Dockerfile gives it write access to the database.
- SQLite ships in the image: POST inserts **vanish** when a new Pod or build starts from the
  database packaged in that image. Keep the original database on your computer too.
  That is accepted in this assignment.
- All members of the same CSC project can see each other's Rahti projects. Do not change other people's projects.
- After the course, delete your project: *Project → Actions → Delete project*.
