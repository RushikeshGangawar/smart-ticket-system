# 🚆 Mumbai Local Smart Railway Ticket System

Fully **offline, free, Flask-based** smart ticket booking system for Mumbai Local Railway.
All fares use a **pre-computed lookup matrix** — zero distance-slab logic at runtime.

---

## ✨ Features

| Feature | Details |
|---|---|
| **114 Stations** | Western, Central, Harbour, Trans-Harbour lines |
| **6,441 Fare Pairs** | Every From→To pair pre-computed in `FARE_LOOKUP` |
| **Official-like Fares** | ₹5–₹50, seeded once from distance slabs, served via O(1) dict lookup |
| **QR Code Tickets** | Auto-generated PNG for every booking |
| **Geolocation** | Browser GPS → nearest station (Haversine, no Google Maps) |
| **Admin Dashboard** | Live stats, revenue, Chart.js graphs |
| **Data Science** | `analytics.py` → 6-panel matplotlib dashboard |
| **Fare Export** | `export_fares.py` → JSON, Python dict, MongoDB-ready list |
| **SQLite Storage** | Fully local, no cloud, no paid APIs |

---

## 🚀 Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run
python app.py

# 3. Open
http://127.0.0.1:5000        ← Book tickets
http://127.0.0.1:5000/admin  ← Admin dashboard
```

---

## 📁 Project Structure

```
mumbai_railway/
├── app.py                    ← Flask server (main)
├── requirements.txt
├── export_fares.py           ← Export fare matrix (JSON / Python / MongoDB)
├── analytics.py              ← Data science charts
├── README.md
├── railway.db                ← SQLite (auto-created on first run)
├── data/
│   ├── __init__.py
│   └── stations.py           ← 114 stations + FARE_LOOKUP matrix + API
├── fare_data/                ← Created by export_fares.py
│   ├── fare_matrix.json      ← {from: {to: fare}}
│   ├── fare_list.json        ← [{from, to, fare}]  MongoDB-ready
│   └── fare_matrix.py        ← Python dict literal
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── ticket.html
└── static/
    └── qrcodes/              ← Generated QR PNG files
```

---

## 🎯 Fare Lookup Architecture

```
App Request:  from_id="W01"  to_id="W16"
                     ↓
              FARE_LOOKUP[(W01, W16)]   ← O(1) dict lookup
                     ↓
              Returns: ₹20
```

**No distance calculation happens at booking time.**
The `FARE_LOOKUP` dict is built once at module import using track-distance slabs,
then every query is an instant dictionary lookup.

### Fare Slab Reference (used only at build time)

| Distance | Fare |
|---|---|
| 0–3 km | ₹5 |
| 4–6 km | ₹10 |
| 7–12 km | ₹15 |
| 13–20 km | ₹20 |
| 21–30 km | ₹15 |
| 31–45 km | ₹30 |
| 46–60 km | ₹35 |
| 61–80 km | ₹40 |
| 81–100 km | ₹45 |
| 100+ km | ₹50 |

---

## 📤 Export Fare Data

```bash
python export_fares.py
```

Generates `fare_data/` with three formats:

**fare_matrix.json** (nested):
```json
{
  "Churchgate": {
    "Andheri": 20,
    "Borivali": 30,
    "Virar": 35
  }
}
```

**fare_list.json** (flat, MongoDB-ready):
```json
[
  {"from": "Andheri", "to": "Borivali", "fare": 15},
  {"from": "Churchgate", "to": "Andheri", "fare": 20}
]
```

**fare_matrix.py** (Python dict):
```python
from fare_data.fare_matrix import FARE_MATRIX
fare = FARE_MATRIX["Churchgate"]["Andheri"]  # → 20
```

---

## 📊 Data Science Analytics

```bash
pip install pandas matplotlib
python analytics.py
```

Outputs `reports/analytics_dashboard.png` with 6 charts:
daily bookings, revenue trend, fare distribution, tickets by line,
bookings by hour, and top departure stations.

---

## 🛠 Tech Stack (100% Free)

- **Python 3.9+** · **Flask 3** · **SQLite** · **qrcode + Pillow**
- **Chart.js 4** (CDN) · **pandas + matplotlib** (optional)
- No Node.js · No npm · No paid APIs · No Google Maps

---

## 🔒 Privacy

All data stays on your machine. No external API calls. No tracking.

*Fare data is official-like and approximate. For simulation/educational use.*
