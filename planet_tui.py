"""
Planet_UI a TUI to explore the solar system
"""
import math
import os
import time
import random
import calc
from skyfield.api import load
import assets
import tui_elements

ts = load.timescale()
the_time = ts.now()
size = os.get_terminal_size()
screen_width = size.columns 
screen_height = size.lines - 3

distance_unit = "km"
velocity_unit = "km"

commands = {"h": "type h to be sent to the help page",
            "dateset": "prompts you to set set specific date or set date as the current date",
            "timeset": "prompts you to set specific time or set time as the current time",
            "unitset": "prompts for what velocity and distance units to display, valid units include {km, mi, au, light-seconds, or light-minutes",
            "animate": "animate the solar system, prompts user for how fast and in what direction to iterate time",
            "goto": "prompts for destination ex.{mars, venus, solarsystem} and navigates to that page"}

page_info = []
grid = []
page_specifier = 0

def planet_page(planet_id):
    os.system("cls")
    moon_counts = []
    tui_elements.text_box(grid, 15, 2, 60, 25, assets.planet_names[planet_id - 1])
    tui_elements.text_box(grid, 5, 9, 65, 35, assets.planet_imgs[planet_id - 1])
    planet_type = ""
    if planet_id < 5:
        planet_type = "Terrestrial Planet"
    elif planet_id < 7:
        planet_type = "Gas Giant"
    else:
        planet_type = "Ice Giant"
    
    tui_elements.text_box(grid, 70, 5, 40, 3, f"Planet Type: {planet_type}", True)
    tui_elements.text_box(grid, 70, 8, 46, "stretch", "Description", True, "fill")
    tui_elements.text_box(grid, 70, 10, 46, "stretch", assets.planet_description[planet_id - 1], True, "fill")
    
    tui_elements.text_box(grid, 120, 5, 50, 4,"Planetary data accessed from JPL ephemeris", True, "fill")
    tui_elements.text_box(grid, 120, 8, 50, 4,f"Ephermis used: {calc.ephem}", True, "fill")
    tui_elements.text_box(grid, 120, 11, 50, 4,f"Time set to {the_time.utc_strftime()}", True, "fill")    
    
    tui_elements.text_box(grid, 120, 25, 50, 3,f"Distances", True, "fill")    
    tui_elements.text_box(grid, 120, 30, "stretch", 18, calc.planet_dists(planet_id, distance_unit, the_time), True)
    tui_elements.text_box(grid, 120, 27, "stretch", 4, calc.sun_dist(planet_id, distance_unit, the_time), True)
    
    
    tui_elements.text_box(grid, 70, 25, 40, 3,f"Velocity", True, "fill")
    tui_elements.text_box(grid, 70, 27, 40, 5,f"{calc.calc_velocity(planet_id, velocity_unit, the_time)}", True, "fill")
def go_to():
    planets = ["mercury","venus","earth","mars","jupiter","saturn","uranus","neptune"]
    global page_info, page_specifier
    while True:
        go = str(input("go to where? (q to quit): ")).lower()
        if go == "q":
            os.system("cls")
            break
        
        if go in planets:
            page_info = [planet_page]
            page_specifier = planets.index(go) + 1      
            break
        if go == "solarsystem":
            page_specifier = 0
            page_info = [solar_system]
            break

        else:
            print(f"invalid, program does not recognize {go} as a place to go to. Try again")
            
def set_new_date():
    while True:
        inp1 = input("Enter d to set date or n for the current date: ")
        if inp1 == "n" or inp1 == "d":
            break
        else:
            print("Invalid input enter n or d")
        
    if inp1 == "n":
        return ts.now()
    else:
        while True:
            try:
                year = int(input("Enter a year from 1850 to 2149: "))
                if year > 1850 and year < 2149:
                    break
                else:
                    print("Invalid year please enter year within range 1850-2149")
            except TypeError:
                print("please enter a number for the year")
        while True:
            try:
                month = int(input("Enter a month from 1 to 12: "))
                if month >= 1 and month <= 12:
                    break
                else:
                    print("Invalid month enter int from 1 to 12")
            except TypeError:
                print("please enter a number for the month: ")
        while True:
            try:
                day = int(input("Enter a day from 1 to 31: "))
                if day < 1 or day > 31:
                    print("invalid day enter day within range of 1 to 31")
                elif month == 2 and (year % 4 != 0) and day > 28:
                    print("invalid day, feburary is only 28 days long on non leap years")
                elif month == 2 and (year % 4 == 0) and day > 29:
                    print("invalid day, feburary is only 29 days long on leap years")
                elif (month == 4 or month == 6 or month == 9 or month == 11) and day > 30:
                        print("invalid day, this month is only 30 days long")
                else:
                    break
            except TypeError:
                print("please enter a number for the day")
        the_hour = the_time.utc.hour
        the_minute = the_time.utc.minute
        the_second = the_time.utc.second
        return ts.utc(year, month, day, the_hour, the_minute, the_second) 
        

def set_new_time():
    while True:
        inp1 = input("Enter t to set time or n for the current time: ")
        if inp1 == "t" or inp1 == "n":
            break
        else:
            print("Invalid input enter t or n")
        
    if inp1 == "n":
        return ts.now()
    else:
        while True:
            try:
                hour = int(input("Enter an hour in military time from 0 to 23: "))
                if hour >= 0 and hour < 23:
                    break
                else:
                    print("Invalid hour please enter a hour within range 0-23")
            except (TypeError, ValueError):
                print("please enter an integer for the hour")
        while True:
            try:
                minute = int(input("Enter a minute from 0 to 59: "))
                if minute >= 0 and minute < 60:
                    break
                else:
                    print("Invalid hour please enter a minute within range 0-59")
            except (TypeError, ValueError):
                print("please enter an integer for the minute")            
        while True:
            try:
                second = int(input("Enter a second from 0 to 59: "))
                if second >= 0 and second < 60:
                    break
                else:
                    print("Invalid second please enter a second within range 0-59")
            except (TypeError, ValueError):
                print("please enter an integer for the second")  
        the_year = the_time.utc.year
        the_month = the_time.utc.month
        the_day = the_time.utc.day
        return ts.utc(the_year, the_month, the_day, hour, minute, second) 
        

def unit_set():
    global distance_unit, velocity_unit
    q = False
    valid_d_units = ["km","mi","au","ls","lm"]
    valid_v_units = ["km","mi","au"]
    dist_units = "[km (kilometers), mi (miles), au (astronomical units), ls (light-seconds), lm (light-minutes]"
    vel_units = "[km (kilometers), mi (miles), au (astronomical units)"
    while True:
        d_unit = str(input("Enter a distance unit or q to quit, u to see distance units: ")).lower()
        if d_unit == "q":
            q = True
            break
        if d_unit == "u":
            print(f"the valid distance units are {valid_d_units}")
        elif d_unit in valid_v_units:
            distance_unit = d_unit
            print(f"Distance Units are now set to {d_unit}")
            break
        else:
            print("invalid input unit not recognized")
    while True:           
        if q:
            break
        else:
            v_unit = str(input("Enter a velocity unit or q to quit, u to see velocity units: ")).lower()
            if v_unit == "q":
                break
            if v_unit == "u":
                print(f"the valid velocity units: {valid_v_units}")
            elif v_unit in valid_v_units:
                velocity_unit = v_unit
                print(f"Velocity units are now set to {v_unit}")
                break
            else:
                print("invalid input unit not recognized")
            
                
def grid_set():
    global grid
    grid = []
    for j in range(screen_height):
        row_arr = []
        for i in range(screen_width):
            row_arr.append(" ")
        grid.append(row_arr)


def grid_call():
    global grid
    for i in range(screen_height):
        for j in range(screen_width):
            print(grid[i][j], end = "")


def screen_clear():
    os.system("cls")
    grid_set()
    grid_call()


def _help():
    os.system("cls")
    com_text = ""
    print("Valid Commands")
    for command, description in commands.items():
        com_text = com_text + f"{command}           {description}"
        tui_elements.text_box(grid, 3, 3, 200, 100, com_text)

def solar_system():
    os.system("cls")
    sun = tui_elements.circle(90, 25, 4,"sun")
    planets = ["place holder",
               tui_elements.circle(60, 20, 3, "Mercury"),
               tui_elements.circle(60, 20, 3,"Venus"),
               tui_elements.circle(60, 20, 3, "Earth"),
               tui_elements.circle(60, 20, 3, "Mars"),
               tui_elements.circle(60, 20, 3, "Jupiter"),
               tui_elements.circle(60, 20, 3, "Saturn"),
               tui_elements.circle(60, 20, 3, "Uranus"),
               tui_elements.circle(60, 20, 3, "Neptune"),
               ]
    grid_set()
    sun.draw(grid)
    for i in range(1, 9):
        pass
        tui_elements.draw_ring(grid, sun, round(4 + i * 3)) 
    for i, planet in enumerate(planets):
        if i > 0:                      
            planet.orbit(sun, round(4 + i * 3), calc.calc_sun_angle(i, the_time), 0)            
            planet.draw(grid)
    tui_elements.text_box(grid, 5, 25, "stretch", "stretch", "Vernal Equinox", False)
    print(f"Aproximation of Angles of planets from Sun as of {the_time.utc_strftime()} accessed from JPL ephemeris {calc.ephem}") 


    def animate_system():
        global the_time
        while True:
            try:
                step = float(input("Enter a float or integer for the step length in days per frame from -15 to 15 with an absolute value above 0.1: ")) 
                if step > -10 and step < 10 and abs(step) > 0.1:
                    break
                else:
                    print("invalid please enter Enter a float or integer for the step length in days per frame from -15 to 15 with an absolute value above 0.1")
            except (ValueError, TypeError):
                print("invalid input enter a number")
        while True:
            grid_set()
            solar_system()
            the_time = the_time + step
            grid_call()
            

if __name__ == "__main__":

    screen_clear()
    while True:
        inp = input("Enter a command, h for help: ")
        if inp in commands:
            if inp == "h":
                page_specifier = 0
                page_info = [_help]
            if inp == "dateset":
                the_time = set_new_date()
                os.system("cls")
                print(f"time set to {the_time.utc_strftime()}")
            if inp == "timeset":
                the_time = set_new_time()
                os.system("cls")
                print(f"time set to {the_time.utc_strftime()}")                
            if inp == "goto":
                go_to()
            if inp == "unitset":
                unit_set()
            if inp == "animate":
                page_info = [animate_system]
        else:
            print("that's not a command")
        grid_set()
        if page_specifier == 0:
            for page in page_info:
                page()
            grid_call()
        else:
            for page in page_info:
                page(page_specifier)
            grid_call()        
