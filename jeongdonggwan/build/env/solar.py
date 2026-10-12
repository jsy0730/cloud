import math, datetime
LAT, LON, TZ = 35.15715, 129.06578, 9.0
def sunpos(y, m, d, hh, mm=0):
    """NOAA solar position. returns (azimuth deg from N clockwise, elevation deg)"""
    dt = datetime.date(y, m, d); N = dt.timetuple().tm_yday
    g = 2 * math.pi / 365 * (N - 1 + (hh + mm / 60 - 12) / 24)
    eqt = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = 0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    tst = (hh * 60 + mm) + eqt + 4 * LON - 60 * TZ
    ha = math.radians(tst / 4 - 180); lat = math.radians(LAT)
    cz = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(ha)
    zen = math.acos(max(-1, min(1, cz))); el = 90 - math.degrees(zen)
    az = math.degrees(math.atan2(math.sin(ha), math.cos(ha) * math.sin(lat) - math.tan(decl) * math.cos(lat))) + 180
    return az % 360, el
DATES = {'동지': (2026, 12, 21), '춘·추분': (2026, 3, 21), '하지': (2026, 6, 21)}
if __name__ == '__main__':
    for k, (y, m, d) in DATES.items():
        print(k, [ (h, round(sunpos(y, m, d, h)[0]), round(sunpos(y, m, d, h)[1], 1)) for h in (7, 9, 12, 15, 17)])
