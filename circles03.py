"""
Circle function made to work with a simple grid
also lets get some rotation
"""
import math
import os
import time

size = os.get_terminal_size()
screen_width = size.columns 
screen_height = size.lines - 1

grid = []

def grid_set():
    global grid
    for j in range(screen_height):
        row_arr = []
        for i in range(screen_width):
            row_arr.append(" ")
        grid.append(row_arr)


def grid_call():
    global grid
    for i in range(screen_height):
        print("".join(grid[i]))


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
                        if grid[self.y + i][self.x + j]:
                            grid[self.y + i][self.x + j] = "█" 
                    except IndexError:
                        pass  
            for k in range(len(self.name)):
                try:
                     if grid[self.y + self.size][self.x + k]:
                        grid[self.y + self.size][self.x + k] = self.name[k] 
                except IndexError:
                    pass          
        def orbit(self, origin, dist, init_ang, speed):
            
            if not hasattr(self, "ang"):
                self.ang = init_ang
            self.x = origin.x + round(math.sin(self.ang) * (dist * 2))
            self.y = origin.y + round(math.cos(self.ang) * dist * 0.9)
            self.ang = self.ang + speed
                
if __name__ == "__main__":
    grid_set()
    sun = circle(80,25,4,"sun")

    
    planets = [circle(60,20,3, "mercury"),
               circle(60,20,3,"venus"),
               circle(60,20,3., "earth"),
               circle(60,20,3, "mars"),
               circle(60,20,3, "jupiter"),
               circle(60,20,3, "saturn"),
               circle(60,20,3, "uranus"),
               circle(60,20,3, "neptune"),
               ]
    
    while True:
        grid = []
        grid_set()
        sun.draw()

        for i, planet in enumerate(planets):
            planet.orbit(sun, 6 + i * 3, i * 10, 0) 
            planet.draw()
        
        print("\033[H", end="")
        grid_call()
        time.sleep(0.05)

