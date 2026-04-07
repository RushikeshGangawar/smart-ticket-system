"""
Mumbai Local Railway — Data Science Analytics
Run: python analytics.py
Generates charts and insights from the booking database.
All libraries are FREE & open-source.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")           # headless – no display needed
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.patches import FancyBboxPatch
    HAS_PANDAS  = True
    HAS_MPL     = True
except ImportError:
    HAS_PANDAS  = False
    HAS_MPL     = False

DB_PATH     = Path(__file__).parent / "railway.db"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ── theme ──────────────────────────────────────────────────────────────────────
DARK_BG  = "#0d0f14"
CARD     = "#1a1e2a"
BORDER   = "#252a38"
ACCENT   = "#f97316"
ACCENT2  = "#fbbf24"
BLUE     = "#3b82f6"
GREEN    = "#22c55e"
PURPLE   = "#a855f7"
TEXT     = "#e8eaf0"
MUTED    = "#6b7280"

def set_dark_style():
    plt.rcParams.update({
        "figure.facecolor":  DARK_BG,
        "axes.facecolor":    CARD,
        "axes.edgecolor":    BORDER,
        "axes.labelcolor":   TEXT,
        "xtick.color":       MUTED,
        "ytick.color":       MUTED,
        "text.color":        TEXT,
        "grid.color":        BORDER,
        "grid.linestyle":    "--",
        "grid.alpha":        0.6,
        "font.family":       "monospace",
        "legend.facecolor":  CARD,
        "legend.edgecolor":  BORDER,
    })

def load_data():
    if not DB_PATH.exists():
        print(f"[WARN] Database not found at {DB_PATH}")
        print("       Run app.py and book some tickets first.")
        return None
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM tickets", conn)
    conn.close()
    if df.empty:
        print("[INFO] No tickets found – book some first!")
        return None
    # parse date
    df["booked_dt"] = pd.to_datetime(df["booked_at"], format="%d %b %Y, %I:%M:%S %p", errors="coerce")
    df["date"]      = df["booked_dt"].dt.date
    df["hour"]      = df["booked_dt"].dt.hour
    print(f"[OK]  Loaded {len(df)} tickets from database")
    return df


def generate_dashboard(df):
    set_dark_style()
    fig = plt.figure(figsize=(18, 12), facecolor=DARK_BG)
    fig.suptitle("Mumbai Local Railway — Booking Analytics", color=TEXT, fontsize=16, fontweight="bold", y=.98)

    gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=.45, wspace=.35)

    # 1. Daily bookings bar
    ax1 = fig.add_subplot(gs[0, :2])
    daily = df.groupby("date").agg(tickets=("id","count"), revenue=("fare","sum")).reset_index()
    ax1.bar(daily["date"].astype(str), daily["tickets"], color=ACCENT, alpha=.85, width=.6)
    ax1.set_title("Daily Bookings", color=TEXT, fontsize=11)
    ax1.tick_params(axis="x", rotation=45, labelsize=7)
    ax1.yaxis.grid(True); ax1.set_axisbelow(True)

    # 2. Pie by line
    ax2 = fig.add_subplot(gs[0, 2])
    line_counts = df["from_line"].value_counts()
    colors_pie  = [ACCENT, BLUE, GREEN]
    wedges, texts, autotexts = ax2.pie(
        line_counts.values, labels=line_counts.index,
        colors=colors_pie[:len(line_counts)],
        autopct="%1.0f%%", startangle=90,
        wedgeprops=dict(edgecolor=DARK_BG, linewidth=2),
        textprops=dict(color=TEXT, fontsize=9)
    )
    for at in autotexts: at.set_color(DARK_BG); at.set_fontweight("bold")
    ax2.set_title("Tickets by Line", color=TEXT, fontsize=11)

    # 3. Revenue over time
    ax3 = fig.add_subplot(gs[1, :2])
    daily_rev = df.groupby("date")["fare"].sum().reset_index()
    ax3.fill_between(daily_rev["date"].astype(str), daily_rev["fare"], alpha=.25, color=ACCENT2)
    ax3.plot(daily_rev["date"].astype(str), daily_rev["fare"], color=ACCENT2, linewidth=2, marker="o", markersize=4)
    ax3.set_title("Daily Revenue (₹)", color=TEXT, fontsize=11)
    ax3.tick_params(axis="x", rotation=45, labelsize=7)
    ax3.yaxis.grid(True); ax3.set_axisbelow(True)

    # 4. Fare distribution
    ax4 = fig.add_subplot(gs[1, 2])
    fare_counts = df["fare"].value_counts().sort_index()
    ax4.bar(fare_counts.index.astype(str), fare_counts.values, color=BLUE, alpha=.85)
    ax4.set_title("Fare Distribution", color=TEXT, fontsize=11)
    ax4.set_xlabel("Fare (₹)", color=MUTED, fontsize=9)
    ax4.yaxis.grid(True); ax4.set_axisbelow(True)

    # 5. Bookings by hour
    ax5 = fig.add_subplot(gs[2, :2])
    hourly = df.groupby("hour").size().reset_index(name="count")
    ax5.bar(hourly["hour"], hourly["count"], color=PURPLE, alpha=.85, width=.7)
    ax5.set_title("Bookings by Hour of Day", color=TEXT, fontsize=11)
    ax5.set_xlabel("Hour", color=MUTED, fontsize=9)
    ax5.set_xticks(range(0,24))
    ax5.yaxis.grid(True); ax5.set_axisbelow(True)

    # 6. Top 10 routes
    ax6 = fig.add_subplot(gs[2, 2])
    top = df.groupby("from_name")["id"].count().nlargest(8).reset_index()
    top.columns = ["station","count"]
    ax6.barh(top["station"], top["count"], color=GREEN, alpha=.85)
    ax6.set_title("Top Departure Stations", color=TEXT, fontsize=11)
    ax6.xaxis.grid(True); ax6.set_axisbelow(True)
    ax6.tick_params(axis="y", labelsize=8)

    out = REPORTS_DIR / "analytics_dashboard.png"
    plt.savefig(out, dpi=120, bbox_inches="tight", facecolor=DARK_BG)
    plt.close()
    print(f"[OK]  Dashboard saved → {out}")
    return out


def print_text_report(df):
    print("\n" + "="*60)
    print("  MUMBAI LOCAL RAILWAY — TEXT ANALYTICS REPORT")
    print("="*60)
    print(f"  Total Tickets   : {len(df)}")
    print(f"  Total Revenue   : ₹{df['fare'].sum():,}")
    print(f"  Average Fare    : ₹{df['fare'].mean():.1f}")
    print(f"  Max Fare        : ₹{df['fare'].max()}")
    print(f"  Min Fare        : ₹{df['fare'].min()}")
    print()
    print("  Bookings by Line:")
    for line, cnt in df["from_line"].value_counts().items():
        rev = df[df["from_line"]==line]["fare"].sum()
        print(f"    {line:<12} {cnt:>5} tickets   ₹{rev:,} revenue")
    print()
    print("  Top 5 Routes:")
    top = df.groupby(["from_name","to_name"]).agg(cnt=("id","count"),rev=("fare","sum")).reset_index().nlargest(5,"cnt")
    for _, r in top.iterrows():
        print(f"    {r['from_name']} → {r['to_name']}  ({r['cnt']} tickets, ₹{r['rev']})")
    print()
    print("  Fare Tier Distribution:")
    for fare, cnt in sorted(df["fare"].value_counts().items()):
        bar = "█" * (cnt * 20 // max(df["fare"].value_counts()))
        print(f"    ₹{fare:>3}  {bar:<22} {cnt}")
    print("="*60)


if __name__ == "__main__":
    if not HAS_PANDAS:
        print("[ERR] pandas not installed. Run: pip install pandas matplotlib")
        exit(1)

    df = load_data()
    if df is None:
        exit(0)

    print_text_report(df)

    if HAS_MPL:
        out = generate_dashboard(df)
        print(f"\n  📊 Open the chart: {out}\n")
    else:
        print("[WARN] matplotlib not installed, skipping charts.")
