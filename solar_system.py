"""
Live accurate solar system
"""
import math
import os
import time
import random
import angle_calc
from skyfield.api import load
import pyfiglet
import assets

ts = load.timescale()
the_time = ts.now()

size = os.get_terminal_size()
screen_width = size.columns 
screen_height = size.lines - 2

commands = ["h","timeset","solarsystem","goto","show"]

page_info = []
grid = []

class text_box:
    def __init__(self,x, y, w, h, message, has_border):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.message = message
        self.has_border = has_border
    
    def draw(self):
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
def mercury():
    os.system("cls")
    text1 = assets.mercury
    text_box1 = text_box(10,2,100,25,text1,False)
    text_box1.draw()


def venus():
    print("venus")


def earth():
    print("earth")


def mars():
    print("mars")

places_to_go = ["mercury","venus","earth","mars","jupiter","saturn","uranus"]


def go_to():
    global page_info
    while True:
        go = input("go to where?: ").lower()
        if go in places_to_go:
            if go == "mercury":
                page_info = [mercury]
            elif go == "venus":
                page_info = [venus]        
            elif go == "earth":
                page_info = [earth]
            elif go == "mars":
                page_info = [mars]
            elif go == "jupiter":
                page_info = [jupiter]
            elif go == "saturn":
                page_info = [saturn]
            elif go == "uranus":
                page_info = [uranus]
            elif go == "neptune":
                page_info = [neptune]
            break
        else:
            print(f"invalid, program does not recognize {go} as a place to go to. Try again")
            
def set_new_time():
    year = 0
    month = 0
    day = 0
    while True:
        inp1 = input("Enter d to set date or n for the current time: ")
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
        return ts.utc(year, month, day, 0, 0, 0) 
        
        
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
        print("".join(grid[i]))

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
                        if grid[(self.y - self.size//2) + i][self.x + j]:
                            grid[(self.y - self.size//2) + i][self.x + j] = "█" 
                    except IndexError:
                        pass  
            for k in range(len(self.name)):
                try:
                     if grid[(self.y - self.size//2) + self.size][self.x + k]:
                        grid[(self.y - self.size//2) + self.size][self.x + k] = self.name[k] 
                except IndexError:
                    pass          
        def orbit(self, origin, dist, init_ang, speed):  
            if not hasattr(self, "ang"):
                self.ang = init_ang * math.pi / 180
            self.x = round(origin.x + math.cos(self.ang) * 2 * dist)
            self.y = round(origin.y - math.sin(self.ang) * 0.9 * dist)
            self.ang = self.ang + speed

def solar_system():
    os.system("cls")
    sun = circle(80,24,4,"sun")
    planets = ["place holder",
               circle(60,20,3, "mercury"),
               circle(60,20,3,"venus"),
               circle(60,20,3., "earth"),
               circle(60,20,3, "mars"),
               circle(60,20,3, "jupiter"),
               circle(60,20,3, "saturn"),
               circle(60,20,3, "uranus"),
               circle(60,20,3, "neptune"),
               ]
    grid_set()
    sun.draw()
    for i, planet in enumerate(planets):
        if i > 0:
            planet.orbit(sun, round(6 + i * 2.5), angle_calc.calc_angle(i, the_time), 0) 
            planet.draw()

        
        
if __name__ == "__main__":
    """
    screen_clear()
    while True:
        inp = input("Enter a command, h for help: ")
        if inp in commands:
            if inp == "solarsystem":
                page_info = [solar_system]
            if inp == "h":
                print("These are the valid commands: ")
                for com in commands:
                    print(com)
            if inp == "timeset":
                the_time = set_new_time()
                os.system("cls")
                print(f"time set to {the_time.utc_strftime()}")
            if inp == "goto":
                go_to()
        else:
            print("that's not a command")
        grid_set()
        for page in page_info:
            page()
        grid_call()
        """
    grid_set()
    mercury()
    grid_call()