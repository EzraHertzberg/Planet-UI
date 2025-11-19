import math
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
ephem = 'de430_1850-2150.bsp'
planets = load(ephem)  # ephemeris DE430
ts = load.timescale()
the_time = ts.now()


def calc_angle(planet_id,t):
    position = planets[planet_id].at(t)
    x, y, z = position.frame_xyz(ecliptic_frame).au
    angle = (180/math.pi) * math.atan2(y, x)
    return angle


def calc_dist(planet_id1, planet_id2, t):
    astrometric = planets[planet_id1].at(t).observe(planets[planet_id2])
    ra, dec, distance = astrometric.radec()
    return distance


def gen_dists(planet_id, unit, t):
    dists = ""
    for i in range(8):
        if i !=  planet_id:
            if unit == "km":
                dist = calc_dist(planets[planet_id - 1], planets[i], t).km
            elif unit == "mi":
                dist = calc_dist(planets[planet_id - 1], planets[i], t).mi
            else:
                dist = calc_dist(planets[planet_id - 1], planets[i], t)
    dists = dists + f"\n{dist}"

if __name__ == "__main__":
    print(gen_dists(1, 2, the_time))