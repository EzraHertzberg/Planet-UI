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


def calc_dist(planet_id1, planet_id2, unit, t):
    astrometric = planets[planet_id1].at(t).observe(planets[planet_id2])
    ra, dec, distance = astrometric.radec()
    if unit == "km":
        dist_f = '{:,.0f} km'.format(distance.km)
    elif unit == "mi":
        dist_f = '{:,.0f} mi'.format(distance.km * 0.621371)
    elif unit == "ls":
        dist_f = '{:,.0f} light-seconds'.format(distance.km * (1/299792))
    elif unit == "lm":
        dist_f = '{:,.0f} light-minutes'.format(distance.km * (1/(60*299792)))                
    else:
        dist_f = '{:,.3f} au'.format(distance.au)    
    return dist_f


planet_names = ["","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune"]


def sun_dist(planet_id, unit, t):
    dist = calc_dist(planet_id, 10, unit, t)
    return f"{planet_names[planet_id]} is {dist} away from the Sun" 

def planet_dists(planet_id, unit, t):
    dists = ""
    for i in range(1, 9):
        if i !=  planet_id:
            dist = calc_dist(planet_id, i, unit, t)            
            dists = dists + f"\n{planet_names[planet_id]} is {dist} away from {planet_names[i]}\n"
    return(f"Distances of {planet_names[planet_id]} from all planets: \n" + dists)


if __name__ == "__main__":
    print(sun_dist(3,"au", the_time))
    #print(planets)