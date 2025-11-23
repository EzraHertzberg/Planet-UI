import math
from skyfield.api import load
from skyfield.framelib import ecliptic_frame
ephem = 'de430_1850-2150.bsp'
planets = load(ephem)  # ephemeris DE430
ts = load.timescale()
the_time = ts.now()


def calc_angle(planet_id, t):
    position = planets[planet_id].at(t)
    x, y, z = position.frame_xyz(ecliptic_frame).au
    angle = (180/math.pi) * math.atan2(y, x)
    return angle


def calc_dist(planet_id1, planet_id2, t):
    astrometric = planets[planet_id1].at(t).observe(planets[planet_id2])
    ra, dec, distance = astrometric.radec()
    return distance


planet_names = ["","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]


def sun_dist(planet_id, t):
    dist = calc_dist(planet_id, 10, t)
    return f"Distance from {planet_names[planet_id]} to Sun \n {dist}" 


def gen_dists(planet_id, unit, t):
    dists = ""
    for i in range(1, 9):
        if i !=  planet_id:
            dist = calc_dist(planet_id, i, t)            
            if unit == "km":
                dist_f = '{:,.0f} km'.format(dist.km)
            elif unit == "mi":
                dist_f = '{:,.0f} mi'.format(dist.km * 0.621371)
            elif unit == "ls":
                dist_f = '{:,.0f} light-seconds'.format(dist.km * (1/299792))
            elif unit == "lm":
                dist_f = '{:,.0f} light-minutes'.format(dist.km * (1/(60*299792)))                
            else:
                dist_f = '{:,.3f} au'.format(dist.au)
            dists = dists + f"\n{planet_names[planet_id]} is {dist_f} away from {planet_names[i]}\n"
    return(f"Distances of {planet_names[planet_id]} from all planets: \n" + dists)


if __name__ == "__main__":
    #print(calc_dist(3, 1, the_time))
    print(planets)