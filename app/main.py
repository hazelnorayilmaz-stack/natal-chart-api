from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import swisseph as swe

app = FastAPI(title="Natal Chart API")

class ChartReq(BaseModel):
    birth_date: str  # YYYY-MM-DD
    birth_time: str  # HH:MM
    lat: float
    lon: float
    timezone: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chart")
def chart(req: ChartReq):
    # Swiss Ephemeris path (render-build.sh bunu doldurur)
    swe.set_ephe_path("ephe")

    # Local -> UTC (DST doğru)
    y, m, d = map(int, req.birth_date.split("-"))
    hh, mm = map(int, req.birth_time.split(":"))
    local = datetime(y, m, d, hh, mm, tzinfo=ZoneInfo(req.timezone))
    utc = local.astimezone(timezone.utc)

    jd = swe.julday(
        utc.year, utc.month, utc.day,
        utc.hour + utc.minute / 60.0
    )

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO,
    }

    out = {}
    for name, pid in planets.items():
        lon, lat, dist = swe.calc_ut(jd, pid)[0][:3]
        out[name] = round(lon % 360, 6)

    cusps, ascmc = swe.houses(jd, req.lat, req.lon)
    houses = {f"house_{i}": round(cusps[i], 6) for i in range(1, 13)}

    return {
        "utc": utc.isoformat(),
        "planets": out,
        "angles": {
            "ASC": round(ascmc[0], 6),
            "MC": round(ascmc[1], 6),
        },
        "houses": houses,
    }
