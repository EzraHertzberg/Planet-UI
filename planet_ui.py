"""
Live accurate solar system
"""
import textwrap
import math
import os
import time
import random
import calc
from skyfield.api import load
import assets
ts = load.timescale()
the_time = ts.now()
size = os.get_terminal_size()
screen_width = size.columns 
screen_height = size.lines - 3

commands = ["h","timeset","dateset","solarsystem","goto","show"]

page_info = []
grid = []
page_specifier = 0


class text_box:
    def __init__(self, x, y, w, h, message, has_border=False, wrap=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        if not wrap:
            self.message = message.replace("\n","‽")
        elif wrap == "fill":
            wrapped = textwrap.fill(message, self.w - 2)
            wrapped = wrapped.replace("\n","‽")
            self.message = wrapped
            
        self.has_border = has_border
        
        #actual function
        new_line = False
        character = 0
        lines = []
        for j in range(self.h):
            new_line = False
            for i in range(self.w):
                try:
                    if (i == 0 or i == self.w - 1) and self.has_border:
                            grid[self.y + j][self.x + i] = "|"
                    elif (j == 0 or j == self.h - 1) and self.has_border:
                            grid[self.y + j][self.x + i] = "~"
                    elif len(self.message) > character and not new_line:
                        if self.message[character] != "‽":
                            grid[self.y + j][self.x + i] = self.message[character]
                        if self.message[character] != "‽" and not new_line:
                            character += 1
                        else:
                            if self.message[character] == "‽":
                                character += 1
                            new_line = True
                except IndexError:
                    pass

def planet_page(planet_id):
    os.system("cls")
    moon_counts = []
    text1 = assets.planet_names[planet_id - 1]
    text_box(15, 2, 60, 25, text1)
    if planet_id != 6 and planet_id != 7: 
        text_box(5, 10, 65, 35, assets.planet_imgs[planet_id - 1])
    else:
        text_box(5, 7, 65, 35, assets.planet_imgs[planet_id - 1])
    planet_type = ""
    if planet_id < 5:
        planet_type = "Terrestrial Planet"
    elif planet_id < 7:
        planet_type = "Gas Giant"
    else:
        planet_type = "Ice Giant"
    
    text_box(60, 5, 40, 3, f"Planet Type: {planet_type}", True)
    #text_box(60,8,40,3,f"Moon Count as of 2025: {mooncount}",True)    
    text_box(12, 38, 46, 10, assets.planet_description[planet_id - 1], True, "fill")
    text_box(60, 10, 45, 18, calc.planet_dists(planet_id, "km", the_time), True)
    text_box(60, 7, 45, 4, calc.sun_dist(planet_id, "km", the_time), True)

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


class circle:
        def __init__(self,x, y, size, name):
            self.x = x
            self.y = y
            self.size = int(size)
            self.name = name        
        
        def draw(self):
            for i in range(self.size):
                if i < self.size // 2:
                    e = i + self.size//2
                else:
                    e = self.size + self.size//2 -1 - i
                
                for j in range(-e, e):
                    try:
                        grid[(self.y - self.size//2) + i][self.x + j] = "█" 
                    except IndexError:
                        pass  
            for k in range(len(self.name)):
                try:
                    grid[(self.y - self.size//2) + self.size][self.x + k] = self.name[k] 
                except IndexError:
                    pass
                
                
        def orbit(self, origin, dist, init_ang, speed):  
            if not hasattr(self, "ang"):
                self.ang = init_ang * math.pi / 180
            self.x = round(origin.x + math.cos(self.ang) * 1.8 * dist)
            self.y = round(origin.y - math.sin(self.ang) * 0.9 * dist)
            self.ang = self.ang + speed
            
            
def draw_ring(origin, dist):
    for i in range(1,round(360)):
        try:
            x = round(origin.x + math.cos(i) * 1.8 * dist)
            y = round(origin.y - math.sin(i) * 0.9 * dist)
            grid[y][x] = "."
        except IndexError:
            pass    


def solar_system():
    os.system("cls")
    sun = circle(90,25,4,"sun")
    planets = ["place holder",
               circle(60,20, 3, "Mercury"),
               circle(60,20, 3,"Venus"),
               circle(60,20, 3, "Earth"),
               circle(60,20, 3, "Mars"),
               circle(60,20, 3, "Jupiter"),
               circle(60,20, 3, "Saturn"),
               circle(60,20, 3, "Uranus"),
               circle(60,20, 3, "Neptune"),
               ]
    grid_set()
    sun.draw()
    for i in range(1, 9):
        pass
        draw_ring(sun, round(4 + i * 3)) 
    for i, planet in enumerate(planets):
        if i > 0:                      
            planet.orbit(sun, round(4 + i * 3), calc.calc_angle(i, the_time), 0)            
            planet.draw()
    print(f"Angles of planets as of {the_time.utc_strftime()} accessed from JPL ephemeris {calc.ephem}") 
        
        
if __name__ == "__main__":

    screen_clear()
    while True:
        inp = input("Enter a command, h for help: ")
        if inp in commands:
            if inp == "h":
                os.system("cls")
                print("These are the valid commands: ")
                for com in commands:
                    print(com)
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


    """
    grid_set()
    planet_page(5)
    grid_call()
"""