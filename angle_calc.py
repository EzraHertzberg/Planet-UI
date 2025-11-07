import math
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
planets = load('de430_1850-2150.bsp')  # ephemeris DE421

def calc_angle(planet_id,t):
    position = planets[planet_id].at(t)
    x, y, z = position.frame_xyz(ecliptic_frame).au
    angle = (180/math.pi) * math.atan2(y, x)
    return angle

if __name__ == "__main__":
    pass