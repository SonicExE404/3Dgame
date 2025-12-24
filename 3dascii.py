import time
import math
import sys
import msvcrt


def clear():
    sys.stdout.write("\x1b[H")
    
map_data = [
    "############",
    "#          #",
    "#          #",
    "#          #",
    "#          #",
    "#          #",
    "#######    #",
    "#          #",
    "############"
]
floor_tex = [
    "====||====||",
    "====||====||",
    "||||====||||",
    "||||====||||"
]


map_w = len(map_data[0])#|||||
map_h = len(map_data)#----

#player
px = 3.5 
py = 3.5 
pa = 0.0 

def cast_ray(angle):
    x, y = px, py
    for d in range(50):
        next_x = x + math.cos(angle) * 0.1
        next_y = y + math.sin(angle) * 0.1

        if map_data[int(y)][int(next_x)] == "#":
            return d, True   
        if map_data[int(next_y)][int(x)] == "#":
            return d, False  

        x = next_x
        y = next_y

    return 50, True  


def draw_minimap(screen):
    scale = 2 

    start_x = screen_w - map_w * scale
    start_y = screen_h - map_h * scale

    for my in range(map_h):
        for mx in range(map_w):
            char = map_data[my][mx]
            if char == "#":
                draw_char = "#"
            elif char == "$":
                draw_char = "%"
            else:
                draw_char = " "

            for dy in range(scale):
                for dx in range(scale):
                    sx = start_x + mx * scale + dx
                    sy = start_y + my * scale + dy
                    if 0 <= sx < screen_w and 0 <= sy < screen_h:
                        screen[sy][sx] = draw_char

    px_map = int(px * scale) + start_x
    py_map = int(py * scale) + start_y
    if 0 <= px_map < screen_w and 0 <= py_map < screen_h:
        screen[py_map][px_map] = "P"

    fx = int(math.cos(pa) * scale) + px_map
    fy = int(math.sin(pa) * scale) + py_map
    if 0 <= fx < screen_w and 0 <= fy < screen_h:
        screen[fy][fx] = "+"


screen_h = 70
fov = math.pi / 3
screen_w = 225

sys.stdout.write("\x1b[2J")                
half_h = screen_h // 2                      

while True:
    while msvcrt.kbhit():
        k = msvcrt.getch().decode()
        if k == "a":
            pa -= 0.03
        if k == "d":
            pa += 0.03
        if k == "w":
            px += math.cos(pa) * 0.05
            py += math.sin(pa) * 0.05
        if k == "s":
            px -= math.cos(pa) * 0.05
            py -= math.sin(pa) * 0.05

    screen = [[" "] * screen_w for _ in range(screen_h)]

    for col in range(screen_w):
        ray_angle = pa - fov/2 + (col / screen_w) * fov
        dist, vertical = cast_ray(ray_angle)
        wall_h = int(screen_h / (dist * 0.1 + 0.1))

        top = screen_h//2 - wall_h//2
        bottom = screen_h//2 + wall_h//2

        for row in range(screen_h):
            if top < row < bottom:
                if vertical:
                    base_char = "█"
                else:
                    base_char = "▓"

                if dist <= 10:
                    screen[row][col] = base_char   
                elif dist <= 25:
                    screen[row][col] = "▓" if vertical else "▒"
                elif dist <= 35:
                    screen[row][col] = "▒" if vertical else "░"
                else:
                    screen[row][col] = "░"           


    for row in range(half_h + 1, screen_h):
        p = row - half_h
        row_dist = half_h / p

        for col in range(screen_w):
            ray_angle = pa - fov/2 + (col / screen_w) * fov
            fx = px + math.cos(ray_angle) * row_dist
            fy = py + math.sin(ray_angle) * row_dist

            tx = int(fx * len(floor_tex[0])) % len(floor_tex[0])
            ty = int(fy * len(floor_tex)) % len(floor_tex)

            if screen[row][col] == " ":
                screen[row][col] = floor_tex[ty][tx]
    
    draw_minimap(screen)

    clear()
    sys.stdout.write("\n".join("".join(row) for row in screen))
    sys.stdout.flush()

    time.sleep(0.0001)
    
