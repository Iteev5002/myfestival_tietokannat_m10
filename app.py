"""My Festival REST API — M10 starter (CSC Rahti).

FI: Tämä on M10-tehtävän lähtöpohja. GET /api/artists on valmiina mallina;
    toteuta loput TODO-kohdat. Aja paikallisesti:  python app.py
    ja testaa:  python test_endpoints.py http://localhost:8080
EN: This is the M10 starter. GET /api/artists is done as an example;
    implement the remaining TODOs. Run locally:  python app.py
    and test:  python test_endpoints.py http://localhost:8080
"""
import os
import sqlite3
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

app = Flask(__name__)

# FI: Kanta kulkee kontin mukana. Polun voi vaihtaa ympäristömuuttujalla.
# EN: The database ships inside the container. Override the path with an env var.
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "myfestival.db"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # M8: sqlite3 ei valvo FK:ita oletuksena / FKs are off by default
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def health():
    """FI: Rahti ja selain näkevät, että sovellus on pystyssä.
    EN: Lets Rahti and your browser see the app is up."""
    return jsonify(status="ok", endpoints=["/api/artists", "/api/days", "/api/stages",
                                           "/api/artists/<id>/events", "/api/timetable?day=YYYY-MM-DD",
                                           "POST /api/events", "DELETE /api/events/<id>"])


@app.get("/api/artists")
def get_artists():
    conn = get_db()
    rows = conn.execute("SELECT artist_id, name, country FROM Artist ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/api/days")
def get_days():
    """FI: Apuendpoint: festivaalipäivät (tarkistin hakee tästä day_id:n).
    EN: Helper endpoint: festival days (the checker reads day_id from here)."""
    conn = get_db()
    rows = conn.execute("SELECT day_id, date FROM Day ORDER BY date").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/api/stages")
def get_stages():
    """FI: Apuendpoint: lavat. EN: Helper endpoint: stages."""
    conn = get_db()
    rows = conn.execute("SELECT stage_id, name FROM Stage ORDER BY stage_id").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/api/artists/<int:artist_id>/events")
def get_artist_events(artist_id):
    conn = get_db()
    # Tarkistetaan, onko artistia olemassa
    artist = conn.execute("SELECT 1 FROM Artist WHERE artist_id = ?", (artist_id,)).fetchone()
    if not artist:
        conn.close()
        return jsonify(error="Artist not found"), 404

    rows = conn.execute(
        """
        SELECT e.event_id, d.date AS day, s.name AS stage, e.start_time AS starts
        FROM Event e
        JOIN Day d ON e.day_id = d.day_id
        JOIN Stage s ON e.stage_id = s.stage_id
        WHERE e.artist_id = ?
        ORDER BY d.date, e.start_time
        """,
        (artist_id,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.get("/api/timetable")
def get_timetable():
    day = request.args.get("day")  # FI: kyselyparametri ?day=2025-07-05
    conn = get_db()

    if day:
        try:
            datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            conn.close()
            return jsonify(error="Invalid date format, expected YYYY-MM-DD"), 400

    query = """
        SELECT d.date AS date, s.name AS stage, a.name AS artist, e.start_time AS starts, e.end_time AS ends
        FROM Event e
        JOIN Day d ON e.day_id = d.day_id
        JOIN Stage s ON e.stage_id = s.stage_id
        JOIN Artist a ON e.artist_id = a.artist_id
    """
    params = []
    if day:
        query += " WHERE d.date = ?"
        params.append(day)
    query += " ORDER BY d.date, e.start_time"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.post("/api/events")
def create_event():
    body = request.get_json(silent=True)
    if not body or not isinstance(body, dict):
        return jsonify(error="Invalid JSON body"), 400

    artist_id = body.get("artist_id")
    stage_id = body.get("stage_id")
    day_id = body.get("day_id")
    start_dt = body.get("start_dt")

    if artist_id is None or stage_id is None or day_id is None or start_dt is None:
        return jsonify(error="Missing required fields"), 400

    try:
        start_dt_obj = datetime.strptime(start_dt, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify(error="Invalid start_dt format, expected YYYY-MM-DD HH:MM:SS"), 400

    end_dt_obj = start_dt_obj + timedelta(minutes=45)
    end_dt = end_dt_obj.strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    try:
        # Haetaan sopiva event_type_id (esim. 'Keikka' tai ensimmäinen)
        et_row = conn.execute("SELECT event_type_id FROM EventType WHERE name IN ('Keikka', 'performance') LIMIT 1").fetchone()
        if not et_row:
            et_row = conn.execute("SELECT event_type_id FROM EventType LIMIT 1").fetchone()
        event_type_id = et_row[0] if et_row else 1

        cursor = conn.execute(
            """
            INSERT INTO Event (artist_id, stage_id, day_id, event_type_id, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (artist_id, stage_id, day_id, event_type_id, start_dt, end_dt)
        )
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()

        return jsonify(event_id=event_id, artist_id=artist_id, stage_id=stage_id, day_id=day_id, start_dt=start_dt, end_dt=end_dt), 201
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify(error=f"Database integrity error: {str(e)}"), 400
    except Exception as e:
        conn.close()
        return jsonify(error=str(e)), 400


@app.delete("/api/events/<int:event_id>")
def delete_event(event_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM Event WHERE event_id = ?", (event_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()

    if deleted_count == 0:
        return jsonify(error="Event not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)