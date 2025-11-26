import textwrap
import math
#from ascii_magic import AsciiArt

class text_box:
    def __init__(self, grid, x, y, w, h, message, has_border=False, wrap=None):
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
            
        if self.w == "stretch" or self.h == "stretch":
            longest_line = 0
            current_line_len = 0
            line_counter = 1
            for character in self.message:
                current_line_len += 1
                if current_line_len > longest_line:
                    longest_line = current_line_len
                if character == "‽":
                    line_counter += 1
                    current_line_len = 0
            if self.h == "stretch":
                self.h = line_counter + 2
            if self.w == "stretch":
                self.w = longest_line + 2
            
        self.has_border = has_border
        
        #actual function
        new_line = False
        character = 0
        lines = []
        for j in range(self.h):
            new_line = False
            for i in range(self.w):
                try:
                    if (i == 0 or i == self.w - 1) and (j > 0 and j < self.h - 1)and self.has_border:
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
class circle:
        def __init__(self, x, y, size, name):
            self.x = x
            self.y = y
            self.size = int(size)
            self.name = name        
        
        def draw(self, grid):
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
                
                
        def orbit(self, origin, dist, init_ang, speed = None):  
            if not hasattr(self, "ang"):
                self.ang = init_ang * math.pi / 180
            self.x = round(origin.x + math.cos(self.ang) * 1.8 * dist)
            self.y = round(origin.y - math.sin(self.ang) * 0.9 * dist)
            self.ang = self.ang + speed
            
            
def draw_ring(grid, origin, dist):
    for i in range(1,round(360)):
        try:
            x = round(origin.x + math.cos(i) * 1.8 * dist)
            y = round(origin.y - math.sin(i) * 0.9 * dist)
            grid[y][x] = "."
        except IndexError:
            pass
        
if __name__ == "__main__":
    from ascii_magic import AsciiArt
    my_art = AsciiArt.from_image("images/Uranus_clouds.jpg")
    my_art.to_terminal()