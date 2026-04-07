"""
Mumbai Local Smart Railway Ticket System
Flask backend – fully offline, free, no paid APIs
"""

import os, sys, uuid, json, sqlite3, base64, io
from datetime import datetime
from pathlib import Path

# ── ensure local imports work ─────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, render_template, request, jsonify, send_file
try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

from data.stations import STATIONS, compute_fare, get_fare, nearest_station

# ── paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DB_PATH    = BASE_DIR / "railway.db"
QR_DIR     = BASE_DIR / "static" / "qrcodes"
QR_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = "mumbai_local_2025"

# ── database ──────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id   TEXT UNIQUE NOT NULL,
                from_id     TEXT NOT NULL,
                from_name   TEXT NOT NULL,
                from_line   TEXT NOT NULL,
                to_id       TEXT NOT NULL,
                to_name     TEXT NOT NULL,
                to_line     TEXT NOT NULL,
                distance_km REAL NOT NULL,
                fare        INTEGER NOT NULL,
                nearest_stn TEXT,
                nearest_dist REAL,
                session_id  TEXT,
                device_id   TEXT,
                booked_at   TEXT NOT NULL,
                qr_path     TEXT
            )
        """)
        db.commit()

init_db()

# ── helpers ───────────────────────────────────────────────────────────────────
def generate_ticket_id():
    ts  = datetime.now().strftime("%y%m%d%H%M%S")
    uid = uuid.uuid4().hex[:6].upper()
    return f"MR-{ts}-{uid}"

def make_qr(data: str, ticket_id: str) -> str:
    """Generate QR code PNG, return relative URL path."""
    if not HAS_QR:
        return ""
    qr  = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    img      = qr.make_image(fill_color="#1a1a2e", back_color="#ffffff")
    filename = f"{ticket_id}.png"
    img.save(QR_DIR / filename)
    return f"/static/qrcodes/{filename}"

def qr_base64(ticket_id: str) -> str:
    """Return base64 PNG for inline display."""
    path = QR_DIR / f"{ticket_id}.png"
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    stations_json = json.dumps(STATIONS)
    return render_template("index.html", stations_json=stations_json)

@app.route("/api/stations")
def api_stations():
    return jsonify(STATIONS)

@app.route("/api/nearest")
def api_nearest():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
        st, dist = nearest_station(lat, lon)
        return jsonify({"station": st, "distance_km": dist})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/fare")
def api_fare():
    from_id = request.args.get("from")
    to_id   = request.args.get("to")
    if not from_id or not to_id:
        return jsonify({"error": "Missing from/to"}), 400
    result = compute_fare(from_id, to_id)
    return jsonify(result)

@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.get_json(force=True)
    from_id    = data.get("from_id")
    to_id      = data.get("to_id")
    nearest    = data.get("nearest_station", "")
    near_dist  = data.get("nearest_dist", 0.0)
    session_id = data.get("session_id", str(uuid.uuid4()))
    device_id  = data.get("device_id", "WEB-" + uuid.uuid4().hex[:8].upper())

    if not from_id or not to_id:
        return jsonify({"error": "from_id and to_id required"}), 400
    if from_id == to_id:
        return jsonify({"error": "Source and destination cannot be same"}), 400

    fare_info = compute_fare(from_id, to_id)
    if "error" in fare_info:
        return jsonify(fare_info), 400

    ticket_id = generate_ticket_id()
    booked_at = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")

    # QR payload
    qr_payload = (
        f"TICKET:{ticket_id}\n"
        f"FROM:{fare_info['from_station']['name']}\n"
        f"TO:{fare_info['to_station']['name']}\n"
        f"FARE:INR {fare_info['fare']}\n"
        f"DATE:{booked_at}\n"
        f"DEVICE:{device_id}"
    )
    qr_path = make_qr(qr_payload, ticket_id)

    with get_db() as db:
        db.execute("""
            INSERT INTO tickets
              (ticket_id, from_id, from_name, from_line, to_id, to_name, to_line,
               distance_km, fare, nearest_stn, nearest_dist, session_id, device_id,
               booked_at, qr_path)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            ticket_id,
            fare_info["from_station"]["id"],
            fare_info["from_station"]["name"],
            fare_info["from_station"]["line"],
            fare_info["to_station"]["id"],
            fare_info["to_station"]["name"],
            fare_info["to_station"]["line"],
            fare_info["distance_km"],
            fare_info["fare"],
            nearest,
            near_dist,
            session_id,
            device_id,
            booked_at,
            qr_path,
        ))
        db.commit()

    return jsonify({
        "success":    True,
        "ticket_id":  ticket_id,
        "from":       fare_info["from_station"]["name"],
        "from_line":  fare_info["from_station"]["line"],
        "to":         fare_info["to_station"]["name"],
        "to_line":    fare_info["to_station"]["line"],
        "distance_km":fare_info["distance_km"],
        "fare":       fare_info["fare"],
        "nearest_stn":nearest,
        "nearest_dist": near_dist,
        "session_id": session_id,
        "device_id":  device_id,
        "booked_at":  booked_at,
        "qr_b64":     qr_base64(ticket_id),
        "qr_path":    qr_path,
    })

@app.route("/api/tickets")
def api_tickets():
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM tickets ORDER BY id DESC LIMIT 200"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/stats")
def api_stats():
    with get_db() as db:
        total  = db.execute("SELECT COUNT(*) as c FROM tickets").fetchone()["c"]
        rev    = db.execute("SELECT COALESCE(SUM(fare),0) as r FROM tickets").fetchone()["r"]
        by_day = db.execute("""
            SELECT substr(booked_at,1,11) as day, COUNT(*) as cnt, SUM(fare) as rev
            FROM tickets GROUP BY day ORDER BY day DESC LIMIT 30
        """).fetchall()
        by_line = db.execute("""
            SELECT from_line as line, COUNT(*) as cnt FROM tickets GROUP BY from_line
        """).fetchall()
        top_routes = db.execute("""
            SELECT from_name||' → '||to_name as route, COUNT(*) as cnt, SUM(fare) as rev
            FROM tickets GROUP BY from_name, to_name ORDER BY cnt DESC LIMIT 10
        """).fetchall()
    return jsonify({
        "total_tickets": total,
        "total_revenue": rev,
        "by_day":        [dict(r) for r in by_day],
        "by_line":       [dict(r) for r in by_line],
        "top_routes":    [dict(r) for r in top_routes],
    })

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/ticket/<ticket_id>")
def ticket_page(ticket_id):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)
        ).fetchone()
    if not row:
        return "Ticket not found", 404
    t = dict(row)
    t["qr_b64"] = qr_base64(ticket_id)
    return render_template("ticket.html", ticket=t)

if __name__ == "__main__":
    print("🚆  Mumbai Local Railway Ticket System")
    print("🌐  Open: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
