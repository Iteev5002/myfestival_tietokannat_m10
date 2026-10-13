# My Festival API — endpoint-dokumentti / endpoint document

> FI: Täytä tämä pohja ja palauta se Moodleen (Markdown tai PDF, 1–2 sivua). Korvaa kaikki `<…>`-kohdat.
> Esimerkkivastaukset kopioit oman julkisen rajapintasi oikeista vastauksista (selain tai `curl.exe`/`curl`).
>
> EN: Fill in this template and submit it to Moodle (Markdown or PDF, 1–2 pages). Replace every `<…>`.
> Copy the example responses from your own public API's real responses (browser or `curl.exe`/`curl`).

**Tekijä / Author:** <nimi / name>
**Julkinen osoite / Public URL:** `https://<osoitteesi / your-address>.rahtiapp.fi`
**GitHub:** `https://github.com/<käyttäjä / user>/<repo>`
**Tarkistimen tulos / Checker result:** `<NN>/<NN> checks passed` (liitä koko tuloste palautukseen / attach the full output)

---

## 1. Endpointit / Endpoints

| Metodi / Method | Polku / Path | Onnistuu / Success | Virheet / Errors |
|---|---|---|---|
| GET | `/api/artists` | 200 | – |
| GET | `/api/days` | 200 | – |
| GET | `/api/stages` | 200 | – |
| GET | `/api/artists/{id}/events` | 200 | 404 |
| GET | `/api/timetable?day=YYYY-MM-DD` | 200 | 400 |
| POST | `/api/events` | 201 | 400 |
| DELETE | `/api/events/{id}` | 204 | 404 |

## 2. Esimerkit / Examples

Kirjoita jokaisesta endpointista esimerkkikutsu ja (lyhennetty) vastaus. Malli:
For every endpoint, write an example call and a (shortened) response. Example:

### GET /api/artists

```bash
curl https://<osoitteesi>.rahtiapp.fi/api/artists
```
```json
[{"artist_id": 3, "country": "UK", "name": "Adele"}, …]
```

### GET /api/artists/{id}/events
```bash
<kutsu / call>
```
```json
<vastaus / response>
```
Tuntematon id / unknown id → `<tilakoodi ja runko / status code and body>`

### GET /api/timetable?day=YYYY-MM-DD
```bash
<kutsu / call>
```
```json
<vastaus / response>
```
Virheellinen päivämäärä / invalid date → `<tilakoodi ja runko / status code and body>`

### POST /api/events
```bash
curl -X POST https://<osoitteesi>.rahtiapp.fi/api/events \
     -H "Content-Type: application/json" \
     -d '{"artist_id": <id>, "stage_id": <id>, "day_id": <id>, "start_dt": "YYYY-MM-DD HH:MM:SS"}'
```
```json
<vastaus (201) / response (201)>
```
Puuttuva kenttä / missing field → `<…>` · Olematon artist_id / unknown artist_id → `<…>`

### DELETE /api/events/{id}
```bash
<kutsu / call>
```
Onnistuu / success → `<…>` · Tuntematon id / unknown id → `<…>`

## 3. Julkaisu Rahtiin / Deploying to Rahti (3–6 lausetta / sentences)

<FI: Kuvaa omin sanoin build → deployment → route: mitä Rahti teki repostasi ja mistä löysit julkisen osoitteen.
Mainitse yksi ongelma, johon törmäsit, ja miten ratkaisit sen.>
<EN: Describe build → deployment → route in your own words: what Rahti did with your repo and where you found
the public address. Mention one problem you ran into and how you solved it.>

## 4. Tietoturva / Security (2–4 lausetta / sentences)

<FI: Mitä tämä rajapinta tarvitsisi ennen oikeaa tuotantokäyttöä? Miten varmistit, ettei SQL-injektio onnistu?>
<EN: What would this API need before real production use? How did you make sure SQL injection is not possible?>
