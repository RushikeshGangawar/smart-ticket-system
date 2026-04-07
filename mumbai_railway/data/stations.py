"""
Mumbai Local Railway — Complete Station Master  (~150 stations)
Official-like fare lookup matrix: every From→To pair pre-computed.
The app ALWAYS queries FARE_LOOKUP[(from_id, to_id)] — never raw slabs.
"""

# ─────────────────────────────────────────────────────────────────────────────
#  STATION MASTER
# ─────────────────────────────────────────────────────────────────────────────
STATIONS = [
    # WESTERN LINE (Churchgate → Virar)
    {"id":"W01","name":"Churchgate",          "line":"Western",       "lat":18.9353,"lon":72.8264,"km":0.0},
    {"id":"W02","name":"Marine Lines",        "line":"Western",       "lat":18.9433,"lon":72.8236,"km":1.2},
    {"id":"W03","name":"Charni Road",         "line":"Western",       "lat":18.9514,"lon":72.8193,"km":2.3},
    {"id":"W04","name":"Grant Road",          "line":"Western",       "lat":18.9641,"lon":72.8155,"km":3.6},
    {"id":"W05","name":"Mumbai Central",      "line":"Western",       "lat":18.9692,"lon":72.8196,"km":4.5},
    {"id":"W06","name":"Mahalaxmi",           "line":"Western",       "lat":18.9809,"lon":72.8193,"km":5.8},
    {"id":"W07","name":"Lower Parel",         "line":"Western",       "lat":18.9925,"lon":72.8270,"km":7.0},
    {"id":"W08","name":"Prabhadevi",          "line":"Western",       "lat":19.0011,"lon":72.8290,"km":8.0},
    {"id":"W09","name":"Dadar",               "line":"Western",       "lat":19.0183,"lon":72.8422,"km":9.5},
    {"id":"W10","name":"Mumbai Matunga",      "line":"Western",       "lat":19.0303,"lon":72.8436,"km":10.6},
    {"id":"W11","name":"Mahim",               "line":"Western",       "lat":19.0397,"lon":72.8431,"km":11.6},
    {"id":"W12","name":"Bandra",              "line":"Western",       "lat":19.0543,"lon":72.8403,"km":13.2},
    {"id":"W13","name":"Khar Road",           "line":"Western",       "lat":19.0653,"lon":72.8378,"km":14.4},
    {"id":"W14","name":"Santacruz",           "line":"Western",       "lat":19.0784,"lon":72.8352,"km":15.7},
    {"id":"W15","name":"Vile Parle",          "line":"Western",       "lat":19.0965,"lon":72.8492,"km":17.4},
    {"id":"W16","name":"Andheri",             "line":"Western",       "lat":19.1197,"lon":72.8469,"km":19.6},
    {"id":"W17","name":"Jogeshwari",          "line":"Western",       "lat":19.1372,"lon":72.8492,"km":21.3},
    {"id":"W18","name":"Ram Mandir",          "line":"Western",       "lat":19.1486,"lon":72.8433,"km":22.4},
    {"id":"W19","name":"Goregaon",            "line":"Western",       "lat":19.1641,"lon":72.8497,"km":24.0},
    {"id":"W20","name":"Malad",               "line":"Western",       "lat":19.1866,"lon":72.8486,"km":26.3},
    {"id":"W21","name":"Kandivali",           "line":"Western",       "lat":19.2043,"lon":72.8525,"km":28.1},
    {"id":"W22","name":"Borivali",            "line":"Western",       "lat":19.2283,"lon":72.8561,"km":30.6},
    {"id":"W23","name":"Dahisar",             "line":"Western",       "lat":19.2497,"lon":72.8581,"km":32.8},
    {"id":"W24","name":"Mira Road",           "line":"Western",       "lat":19.2811,"lon":72.8694,"km":36.2},
    {"id":"W25","name":"Bhayandar",           "line":"Western",       "lat":19.3003,"lon":72.8506,"km":38.4},
    {"id":"W26","name":"Naigaon",             "line":"Western",       "lat":19.3569,"lon":72.8519,"km":44.5},
    {"id":"W27","name":"Vasai Road",          "line":"Western",       "lat":19.3689,"lon":72.8297,"km":47.8},
    {"id":"W28","name":"Nallasopara",         "line":"Western",       "lat":19.4196,"lon":72.7992,"km":53.2},
    {"id":"W29","name":"Virar",               "line":"Western",       "lat":19.4592,"lon":72.7911,"km":57.5},

    # CENTRAL MAIN LINE (CSMT → Kasara / Karjat)
    {"id":"C01","name":"CSMT",                "line":"Central",       "lat":18.9398,"lon":72.8355,"km":0.0},
    {"id":"C02","name":"Masjid",              "line":"Central",       "lat":18.9467,"lon":72.8367,"km":1.0},
    {"id":"C03","name":"Sandhurst Road",      "line":"Central",       "lat":18.9572,"lon":72.8381,"km":2.2},
    {"id":"C04","name":"Byculla",             "line":"Central",       "lat":18.9711,"lon":72.8328,"km":3.8},
    {"id":"C05","name":"Chinchpokli",         "line":"Central",       "lat":18.9803,"lon":72.8336,"km":4.9},
    {"id":"C06","name":"Currey Road",         "line":"Central",       "lat":18.9908,"lon":72.8333,"km":6.0},
    {"id":"C07","name":"Parel",               "line":"Central",       "lat":19.0000,"lon":72.8389,"km":7.0},
    {"id":"C08","name":"Dadar (CR)",          "line":"Central",       "lat":19.0183,"lon":72.8436,"km":9.0},
    {"id":"C09","name":"Matunga",             "line":"Central",       "lat":19.0275,"lon":72.8597,"km":10.3},
    {"id":"C10","name":"Sion",                "line":"Central",       "lat":19.0397,"lon":72.8625,"km":11.5},
    {"id":"C11","name":"Kurla",               "line":"Central",       "lat":19.0658,"lon":72.8792,"km":14.2},
    {"id":"C12","name":"Vidyavihar",          "line":"Central",       "lat":19.0789,"lon":72.9086,"km":16.2},
    {"id":"C13","name":"Ghatkopar",           "line":"Central",       "lat":19.0861,"lon":72.9081,"km":17.0},
    {"id":"C14","name":"Vikhroli",            "line":"Central",       "lat":19.1069,"lon":72.9253,"km":19.5},
    {"id":"C15","name":"Kanjurmarg",          "line":"Central",       "lat":19.1192,"lon":72.9436,"km":21.4},
    {"id":"C16","name":"Bhandup",             "line":"Central",       "lat":19.1425,"lon":72.9444,"km":23.7},
    {"id":"C17","name":"Nahur",               "line":"Central",       "lat":19.1569,"lon":72.9456,"km":25.2},
    {"id":"C18","name":"Mulund",              "line":"Central",       "lat":19.1728,"lon":72.9581,"km":26.9},
    {"id":"C19","name":"Thane",               "line":"Central",       "lat":19.1894,"lon":72.9742,"km":29.3},
    {"id":"C20","name":"Kalwa",               "line":"Central",       "lat":19.1972,"lon":73.0000,"km":31.5},
    {"id":"C21","name":"Mumbra",              "line":"Central",       "lat":19.1953,"lon":73.0194,"km":33.8},
    {"id":"C22","name":"Diva",                "line":"Central",       "lat":19.1997,"lon":73.0444,"km":36.5},
    {"id":"C23","name":"Kopar",               "line":"Central",       "lat":19.2256,"lon":73.0636,"km":39.2},
    {"id":"C24","name":"Dombivli",            "line":"Central",       "lat":19.2167,"lon":73.0878,"km":41.4},
    {"id":"C25","name":"Thakurli",            "line":"Central",       "lat":19.2200,"lon":73.0997,"km":42.7},
    {"id":"C26","name":"Kalyan",              "line":"Central",       "lat":19.2403,"lon":73.1306,"km":46.0},
    {"id":"C27","name":"Shahad",              "line":"Central",       "lat":19.2178,"lon":73.1589,"km":48.5},
    {"id":"C28","name":"Ambivli",             "line":"Central",       "lat":19.2061,"lon":73.1736,"km":50.3},
    {"id":"C29","name":"Titwala",             "line":"Central",       "lat":19.2536,"lon":73.1928,"km":53.0},
    {"id":"C30","name":"Khadavli",            "line":"Central",       "lat":19.2897,"lon":73.2322,"km":57.5},
    {"id":"C31","name":"Vasind",              "line":"Central",       "lat":19.3392,"lon":73.2806,"km":63.0},
    {"id":"C32","name":"Asangaon",            "line":"Central",       "lat":19.4194,"lon":73.2889,"km":71.0},
    {"id":"C33","name":"Atgaon",              "line":"Central",       "lat":19.4956,"lon":73.3150,"km":78.0},
    {"id":"C34","name":"Khardi",              "line":"Central",       "lat":19.5678,"lon":73.3522,"km":85.0},
    {"id":"C35","name":"Kasara",              "line":"Central",       "lat":19.6753,"lon":73.4608,"km":120.0},
    # Karjat branch
    {"id":"C36","name":"Ulhasnagar",          "line":"Central",       "lat":19.2214,"lon":73.1547,"km":49.0},
    {"id":"C37","name":"Ambernath",           "line":"Central",       "lat":19.1994,"lon":73.1928,"km":53.0},
    {"id":"C38","name":"Badlapur",            "line":"Central",       "lat":19.1603,"lon":73.2578,"km":59.0},
    {"id":"C39","name":"Vitthalwadi",         "line":"Central",       "lat":19.1383,"lon":73.2894,"km":62.4},
    {"id":"C40","name":"Neral",               "line":"Central",       "lat":19.0481,"lon":73.2811,"km":72.0},
    {"id":"C41","name":"Bhivpuri Road",       "line":"Central",       "lat":18.9842,"lon":73.3047,"km":79.0},
    {"id":"C42","name":"Karjat",              "line":"Central",       "lat":18.9167,"lon":73.3250,"km":89.0},

    # HARBOUR LINE (CSMT → Panvel)
    {"id":"H01","name":"CSMT (Harbour)",      "line":"Harbour",       "lat":18.9398,"lon":72.8355,"km":0.0},
    {"id":"H02","name":"Wadi Bunder",         "line":"Harbour",       "lat":18.9503,"lon":72.8411,"km":1.5},
    {"id":"H03","name":"Cotton Green",        "line":"Harbour",       "lat":18.9583,"lon":72.8461,"km":2.6},
    {"id":"H04","name":"Reay Road",           "line":"Harbour",       "lat":18.9653,"lon":72.8478,"km":3.5},
    {"id":"H05","name":"Dockyard Road",       "line":"Harbour",       "lat":18.9697,"lon":72.8547,"km":4.3},
    {"id":"H06","name":"Sandhurst Rd (H)",    "line":"Harbour",       "lat":18.9572,"lon":72.8381,"km":5.2},
    {"id":"H07","name":"Masjid (H)",          "line":"Harbour",       "lat":18.9467,"lon":72.8367,"km":6.1},
    {"id":"H08","name":"Byculla (H)",         "line":"Harbour",       "lat":18.9711,"lon":72.8328,"km":7.5},
    {"id":"H09","name":"Chinchpokli (H)",     "line":"Harbour",       "lat":18.9803,"lon":72.8336,"km":8.8},
    {"id":"H10","name":"Currey Road (H)",     "line":"Harbour",       "lat":18.9908,"lon":72.8333,"km":9.8},
    {"id":"H11","name":"Parel (H)",           "line":"Harbour",       "lat":19.0000,"lon":72.8389,"km":10.8},
    {"id":"H12","name":"GTB Nagar",           "line":"Harbour",       "lat":19.0517,"lon":72.8831,"km":14.0},
    {"id":"H13","name":"Chunabhatti",         "line":"Harbour",       "lat":19.0589,"lon":72.8833,"km":15.0},
    {"id":"H14","name":"Kurla (Harbour)",     "line":"Harbour",       "lat":19.0658,"lon":72.8792,"km":16.3},
    {"id":"H15","name":"Tilak Nagar",         "line":"Harbour",       "lat":19.0703,"lon":72.8972,"km":17.5},
    {"id":"H16","name":"Chembur",             "line":"Harbour",       "lat":19.0625,"lon":72.8992,"km":18.7},
    {"id":"H17","name":"Govandi",             "line":"Harbour",       "lat":19.0739,"lon":72.8994,"km":19.8},
    {"id":"H18","name":"Mankhurd",            "line":"Harbour",       "lat":19.0528,"lon":72.9350,"km":22.5},
    {"id":"H19","name":"Vashi",               "line":"Harbour",       "lat":19.0758,"lon":73.0058,"km":26.0},
    {"id":"H20","name":"Sanpada",             "line":"Harbour",       "lat":19.0681,"lon":73.0089,"km":27.0},
    {"id":"H21","name":"Juinagar",            "line":"Harbour",       "lat":19.0561,"lon":73.0211,"km":28.5},
    {"id":"H22","name":"Nerul",               "line":"Harbour",       "lat":19.0333,"lon":73.0164,"km":31.0},
    {"id":"H23","name":"Seawoods-Darave",     "line":"Harbour",       "lat":19.0164,"lon":73.0225,"km":32.8},
    {"id":"H24","name":"CBD Belapur",         "line":"Harbour",       "lat":19.0181,"lon":73.0389,"km":34.5},
    {"id":"H25","name":"Kharghar",            "line":"Harbour",       "lat":19.0453,"lon":73.0703,"km":37.0},
    {"id":"H26","name":"Mansarovar",          "line":"Harbour",       "lat":19.0539,"lon":73.0861,"km":38.5},
    {"id":"H27","name":"Khandeshwar",         "line":"Harbour",       "lat":19.0611,"lon":73.1050,"km":40.0},
    {"id":"H28","name":"Panvel",              "line":"Harbour",       "lat":18.9894,"lon":73.1175,"km":44.0},

    # TRANS-HARBOUR LINE (Thane → Panvel)
    {"id":"T01","name":"Thane (TH)",          "line":"Trans-Harbour", "lat":19.1894,"lon":72.9742,"km":0.0},
    {"id":"T02","name":"Airoli",              "line":"Trans-Harbour", "lat":19.1583,"lon":72.9986,"km":4.5},
    {"id":"T03","name":"Rabale",              "line":"Trans-Harbour", "lat":19.1347,"lon":73.0097,"km":6.8},
    {"id":"T04","name":"Ghansoli",            "line":"Trans-Harbour", "lat":19.1167,"lon":73.0133,"km":8.6},
    {"id":"T05","name":"Kopar Khairane",      "line":"Trans-Harbour", "lat":19.1039,"lon":73.0161,"km":10.2},
    {"id":"T06","name":"Turbhe",              "line":"Trans-Harbour", "lat":19.0906,"lon":73.0183,"km":11.9},
    {"id":"T07","name":"Sanpada (TH)",        "line":"Trans-Harbour", "lat":19.0681,"lon":73.0089,"km":14.5},
    {"id":"T08","name":"Juinagar (TH)",       "line":"Trans-Harbour", "lat":19.0561,"lon":73.0211,"km":16.0},
    {"id":"T09","name":"Nerul (TH)",          "line":"Trans-Harbour", "lat":19.0333,"lon":73.0164,"km":19.0},
    {"id":"T10","name":"Seawoods (TH)",       "line":"Trans-Harbour", "lat":19.0164,"lon":73.0225,"km":20.8},
    {"id":"T11","name":"Belapur (TH)",        "line":"Trans-Harbour", "lat":19.0181,"lon":73.0389,"km":22.5},
    {"id":"T12","name":"Kharghar (TH)",       "line":"Trans-Harbour", "lat":19.0453,"lon":73.0703,"km":25.0},
    {"id":"T13","name":"Mansarovar (TH)",     "line":"Trans-Harbour", "lat":19.0539,"lon":73.0861,"km":26.5},
    {"id":"T14","name":"Khandeshwar (TH)",    "line":"Trans-Harbour", "lat":19.0611,"lon":73.1050,"km":28.0},
    {"id":"T15","name":"Panvel (TH)",         "line":"Trans-Harbour", "lat":18.9894,"lon":73.1175,"km":32.0},
]


# ─────────────────────────────────────────────────────────────────────────────
#  FARE SLABS — used ONCE at startup to seed FARE_LOOKUP.
#  The app never calls this directly — always use FARE_LOOKUP.
# ─────────────────────────────────────────────────────────────────────────────
_FARE_SLABS = [
    (  3,  5),
    (  6, 10),
    ( 12, 15),
    ( 20, 20),
    ( 30, 15),
    ( 45, 30),
    ( 60, 35),
    ( 80, 40),
    (100, 45),
    (999, 50),
]

def _slab_fare(km: float) -> int:
    for max_km, fare in _FARE_SLABS:
        if km <= max_km:
            return fare
    return 50


# ─────────────────────────────────────────────────────────────────────────────
#  BUILD COMPLETE FARE LOOKUP MATRIX AT IMPORT TIME
#  Key  : (from_id, to_id)  — symmetric
#  Value: int  fare in ₹
#
#  Distance logic:
#    Same-line pairs  → km difference along track (accurate)
#    Cross-line pairs → Haversine × 1.30 (track-approximation)
# ─────────────────────────────────────────────────────────────────────────────
def _build_fare_lookup() -> dict:
    import math

    def haversine(la1, lo1, la2, lo2) -> float:
        R = 6371
        d1 = math.radians(la2 - la1)
        d2 = math.radians(lo2 - lo1)
        a  = (math.sin(d1 / 2) ** 2
              + math.cos(math.radians(la1)) * math.cos(math.radians(la2))
              * math.sin(d2 / 2) ** 2)
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    lookup: dict = {}
    ids = [s["id"] for s in STATIONS]
    st  = {s["id"]: s for s in STATIONS}

    for i, a_id in enumerate(ids):
        for b_id in ids[i + 1:]:
            a, b = st[a_id], st[b_id]
            if a["line"] == b["line"]:
                dist = abs(a["km"] - b["km"])
            else:
                dist = haversine(a["lat"], a["lon"], b["lat"], b["lon"]) * 1.30
            fare = _slab_fare(dist)
            lookup[(a_id, b_id)] = fare
            lookup[(b_id, a_id)] = fare
        lookup[(a_id, a_id)] = 0   # same station → ₹0

    return lookup


# Pre-built at import — instant O(1) lookups at runtime
FARE_LOOKUP: dict = _build_fare_lookup()


# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def get_fare(from_id: str, to_id: str) -> int:
    """Return official-like ₹ fare for a From→To ID pair. O(1)."""
    key = (from_id, to_id)
    if key not in FARE_LOOKUP:
        raise KeyError(f"Unknown station pair: {from_id!r} → {to_id!r}")
    return FARE_LOOKUP[key]


def get_fare_by_name(from_name: str, to_name: str) -> int:
    """Convenience: lookup fare by station name (case-insensitive)."""
    name_to_id = {s["name"].lower(): s["id"] for s in STATIONS}
    fid = name_to_id.get(from_name.lower())
    tid = name_to_id.get(to_name.lower())
    if not fid:
        raise KeyError(f"Station not found: {from_name!r}")
    if not tid:
        raise KeyError(f"Station not found: {to_name!r}")
    return get_fare(fid, tid)


def compute_fare(from_id: str, to_id: str) -> dict:
    """Full fare info dict used by Flask app.  Uses FARE_LOOKUP — no slabs."""
    import math

    st_by_id = {s["id"]: s for s in STATIONS}
    if from_id not in st_by_id or to_id not in st_by_id:
        return {"error": f"Invalid station ID(s): {from_id!r}, {to_id!r}"}
    if from_id == to_id:
        return {"error": "Source and destination are the same station"}

    fare    = get_fare(from_id, to_id)        # ← lookup only, no slabs here
    from_st = st_by_id[from_id]
    to_st   = st_by_id[to_id]

    if from_st["line"] == to_st["line"]:
        dist_km = round(abs(from_st["km"] - to_st["km"]), 1)
    else:
        def hav(la1,lo1,la2,lo2):
            R=6371; d1=math.radians(la2-la1); d2=math.radians(lo2-lo1)
            a=(math.sin(d1/2)**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(d2/2)**2)
            return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        dist_km = round(hav(from_st["lat"],from_st["lon"],to_st["lat"],to_st["lon"])*1.3, 1)

    return {
        "from_station": from_st,
        "to_station":   to_st,
        "distance_km":  dist_km,
        "fare":         fare,
    }


def export_fare_dict() -> dict:
    """Return {from_name: {to_name: fare}} nested dict for JSON export."""
    id_to_name = {s["id"]: s["name"] for s in STATIONS}
    result: dict = {}
    for (a_id, b_id), fare in FARE_LOOKUP.items():
        if a_id == b_id:
            continue
        result.setdefault(id_to_name[a_id], {})[id_to_name[b_id]] = fare
    return result


def export_fare_list() -> list:
    """Return [{from, to, fare}, …] list for MongoDB / JSON import."""
    id_to_name = {s["id"]: s["name"] for s in STATIONS}
    seen: set = set()
    rows: list = []
    for (a_id, b_id), fare in FARE_LOOKUP.items():
        if a_id == b_id:
            continue
        key = tuple(sorted([a_id, b_id]))
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "from": id_to_name[a_id],
            "to":   id_to_name[b_id],
            "fare": fare,
        })
    return sorted(rows, key=lambda r: (r["from"], r["to"]))


def nearest_station(user_lat: float, user_lon: float):
    """Return closest station + distance (km) to given GPS point."""
    import math

    def hav(la1, lo1, la2, lo2):
        R = 6371; d1 = math.radians(la2-la1); d2 = math.radians(lo2-lo1)
        a = math.sin(d1/2)**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(d2/2)**2
        return R*2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    best, best_dist = None, float("inf")
    for stn in STATIONS:
        d = hav(user_lat, user_lon, stn["lat"], stn["lon"])
        if d < best_dist:
            best_dist, best = d, stn
    return best, round(best_dist, 2)
