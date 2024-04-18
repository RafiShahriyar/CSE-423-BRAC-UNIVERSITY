from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math


previous_time = time.time()
W_Width, W_Height = 500,500

dx_stages_dictionary = {}
current_stage = 3

dx_pattern_dictionary = {}
powerups = ['increase_size', 'decrease_size', 'fast_ball', 'slow_ball', "shooter", "unstoppable"]
solid_prob = 0.2


# Define all stages

# Stage 1:
for y in range(380, 321, -20):
    for x in range(100, 351, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", None]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", None]
dx_stages_dictionary[1] = dx_pattern_dictionary


# Stage 2:
dx_pattern_dictionary = {}
pyramid_top = (225, 380)
pyramid_height = 5
for i in range(pyramid_height):
    y = 380 - i*20
    for x in range(pyramid_top[0] - i*50, pyramid_top[0] + i*50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        if rand_num == 0:
            dx_pattern_dictionary[(x, y)] = ["solid", None]
        else:
            dx_pattern_dictionary[(x, y)] = ["hollow", None]
        

dx_stages_dictionary[2] = dx_pattern_dictionary
    

# Constants for the dual-arch pattern
base_center_x = 250  # Center X coordinate for the base of the arches
base_y_top = 220     # Y coordinate for the top arch base
base_y_bottom = 280  # Y coordinate for the bottom arch base
arch_height = 5      # Number of layers in each arch

# Stage 3: Circular pattern using dual arches
dx_pattern_dictionary = {}

# Construct the top arch
for i in range(arch_height):
    y = base_y_top - i * 20  # Decreasing Y coordinate for the top arch
    for x in range(base_center_x - i * 50, base_center_x + i * 50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        block_type = "solid" if rand_num == 0 else "hollow"
        dx_pattern_dictionary[(x, y)] = [block_type, None]

# Construct the bottom arch
for i in range(arch_height):
    y = base_y_bottom + i * 20  # Increasing Y coordinate for the bottom arch
    for x in range(base_center_x - i * 50, base_center_x + i * 50 + 1, 50):
        rand_num = random.randint(0, int(1/solid_prob))
        block_type = "solid" if rand_num == 0 else "hollow"
        dx_pattern_dictionary[(x, y)] = [block_type, None]

dx_stages_dictionary[3] = dx_pattern_dictionary




dx_bat_speed = 30
dx_bat = {
    "x1": 0,
    "y1": 0,
    'width': 100,
    'height': 15
}

dx_ball_center = (250, 30)
dx_ball_radius = 5
dx_ball_speed = (5, 5)
dx_ball_deviation = 5


def assign_powerup(probability):
    global powerups, dx_pattern_dictionary
    rand_num = random.randint(0, int(1/probability))
    if rand_num == 0:
        powerup = random.choice(powerups)
        print(f"Assigned Powerup {powerup}")
        # dx_pattern_dictionary[(x, y)][1] = powerup
    else:
        powerup = None
    return powerup


def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x 
    b = W_Height-y
    return (a,b)

def draw_points(x, y, color):
    glColor3f(*color)
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def midpoint_line(x1, y1, x2, y2, zone, color):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    incE = 2*dy
    incNE = 2*(dy-dx)  
    y = y1
    # print(x1, y1, x2, y2, zone)
    for x in range(x1, x2+1):
        oz_x, oz_y = convertzoneM(x, y, zone)

        draw_points(oz_x , oz_y, color) 
        if d <= 0:
            d += incE
        else:
            d += incNE
            y += 1

def findzone(x1, y1, x2, y2):    
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
        elif dx >= 0 and dy <= 0:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6 
               
def convertzone0(x, y, zone):  
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convertzoneM(x,y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def eight_way_symmetry(x1, y1, x2, y2, color = (1, 1, 0)):
    zone = findzone(x1, y1, x2, y2)
    # print(zone)
    x1, y1 = convertzone0(x1, y1, zone)
    x2, y2 = convertzone0(x2, y2, zone)
    midpoint_line(x1, y1, x2, y2, zone, color)               


def midpoint_circle(radius, color, center = (0,0)):
    x = 0
    y = radius
    d = 1 - radius
    Circlepoints(x, y, color, center)
    while x < y:
        if d < 0:
            d = d + 2*x+3
            x = x+1 
        else:
            d = d + 2*(x-y)+5
            x = x+1
            y = y-1
        Circlepoints(x, y, color, center)   

def Circlepoints(x, y, color, center):
    draw_points(x+center[0], y+center[1], color)
    draw_points(-x+center[0], y+center[1], color)
    draw_points(x+center[0], -y+center[1], color)
    draw_points(-x+center[0], -y+center[1], color)
    draw_points(y+center[0], x+center[1], color)
    draw_points(-y+center[0], x+center[1], color)
    draw_points(y+center[0], -x+center[1], color)
    draw_points(-y+center[0], -x+center[1], color)

def has_collided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])



# Constants
FIXED_TIME_STEP = 1.0 / 60

# Variables to keep track of time
previous_time = time.time()
accumulator = 0.0

def animate():
    global dx_ball_center, dx_ball_speed, dx_ball_radius, dx_bat, dx_ball_deviation, previous_time, accumulator

    current_time = time.time()
    elapsed = current_time - previous_time
    previous_time = current_time
    accumulator += elapsed

    # Process the accumulated time in fixed steps
    while accumulator >= FIXED_TIME_STEP:
        update_game_state()  # This function will contain your current animate logic
        accumulator -= FIXED_TIME_STEP

    glutPostRedisplay()

def update_game_state():
    global dx_ball_center, dx_ball_speed, dx_ball_radius, dx_bat, dx_ball_deviation, current_stage, dx_stages_dictionary

    dx_pattern_dictionary = dx_stages_dictionary[current_stage]

    # Boundary collision checks
    if dx_ball_center[1] - dx_ball_radius <= 0:
        print("Game Over")
    if dx_ball_center[0] + dx_ball_radius > W_Width or dx_ball_center[0] - dx_ball_radius < 0:
        dx_ball_speed = (-dx_ball_speed[0], dx_ball_speed[1])
    if dx_ball_center[1] + dx_ball_radius > W_Height or dx_ball_center[1] - dx_ball_radius < 0:
        dx_ball_speed = (dx_ball_speed[0], -dx_ball_speed[1])

    # Collision detection with block
    for coordinate, block_powerup in dx_pattern_dictionary.items():
        block, powerup = block_powerup
        
        block_box = {"x": coordinate[0], "y": coordinate[1], "width": 50, "height": 20}
    
        if has_collided(block_box, {"x": dx_ball_center[0] - dx_ball_radius, "y": dx_ball_center[1] - dx_ball_radius, "width": 2*dx_ball_radius, "height": 2*dx_ball_radius}):
            if block == "hollow":
                dx_pattern_dictionary.pop(coordinate)

            elif block == "solid":
                dx_pattern_dictionary[coordinate] = ["hollow", None]

            dx_ball_speed = (dx_ball_speed[0], -dx_ball_speed[1])
            break

        
    # Check for stage transition
    if len(dx_pattern_dictionary) == 0:  # All blocks cleared
        next_stage = current_stage + 1
        if current_stage + 1 <= len(dx_stages_dictionary.keys()):
            current_stage += 1
        if next_stage in dx_stages_dictionary:
            load_stage(next_stage)
        else:
            print("Congratulations! All stages completed!")

    # Collision detection with bat
    ball_box = {"x": dx_ball_center[0] - dx_ball_radius, "y": dx_ball_center[1] - dx_ball_radius, "width": 2*dx_ball_radius, "height": 2*dx_ball_radius}
    bat_box = {"x": dx_bat['x1'], "y": dx_bat['y1'], "width": dx_bat['width'], "height": dx_bat['height']}

    if has_collided(ball_box, bat_box):
        # Calculate where the ball hit the bat
        hit_point = dx_ball_center[0]
        bat_center = dx_bat['x1'] + dx_bat['width'] / 2
        offset = hit_point - bat_center
        
        # Modify the angle based on where it hit the bat
        influence = offset / (dx_bat['width'] / 2)  # Normalizing the offset
        new_dx = influence*dx_ball_deviation  # Adjust speed change factor as necessary

        # Reflecting the vertical speed and adjusting horizontal speed
        dx_ball_speed = (new_dx, -dx_ball_speed[1])

    # Update ball position
    dx_ball_center = (dx_ball_center[0] + dx_ball_speed[0], dx_ball_center[1] + dx_ball_speed[1])
    glutPostRedisplay()

def keyboardListener(key, x, y):
    if key==b' ':
        print("Space pressed")
    if key==b'a':
        print("a pressed")

    if key==b'd':
        print("d pressed")

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global dx_bat_speed
    if key==GLUT_KEY_RIGHT:
        if dx_bat['x1'] + dx_bat['width'] < 500:
            dx_bat['x1'] += dx_bat_speed
        print("Right arrow pressed")

    elif key==GLUT_KEY_LEFT:
        if dx_bat['x1'] > 0:
            dx_bat['x1'] -= dx_bat_speed
        print("Left arrow pressed")



    glutPostRedisplay()

def mouseListener(button, state, x, y):
    if button==GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            pass




def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()




def draw_rectangle_block(rectangle_block,color):
    x1, y1 = rectangle_block['x1'], rectangle_block['y1']
    x2, y2 = x1 + rectangle_block['width'], y1
    x3, y3 = x2, y1 + rectangle_block['height']
    x4, y4 = x1, y1 + rectangle_block['height']
    eight_way_symmetry(x1, y1, x2, y2, color)
    eight_way_symmetry(x2, y2, x3, y3, color)
    eight_way_symmetry(x3, y3, x4, y4, color)
    eight_way_symmetry(x4, y4, x1, y1, color)

def draw_rectangle_block_filled(rectangle_block, color):
    x1, y1 = rectangle_block['x1'], rectangle_block['y1']
    width = rectangle_block['width']
    height = rectangle_block['height']

    for y in range(y1, y1 + height):
        for x in range(x1, x1 + width):
            draw_points(x, y, color)


def draw_line(x1, y1, x2, y2, color):
    eight_way_symmetry(x1, y1, x2, y2, color)

def load_stage(stage_number):
    global dx_pattern_dictionary, dx_stages_dictionary, current_stage
    if stage_number in dx_stages_dictionary:
        dx_pattern_dictionary = dx_stages_dictionary[stage_number]
        current_stage = stage_number
    else:
        print("Stage not found:", stage_number)



def showScreen():
    global rectangle_block, dx_bat, dx_ball_center, dx_pattern_dictionary, current_stage
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    load_stage(current_stage)

    # Draw all blocks for the current stage
    for coordinate, block_info in dx_pattern_dictionary.items():
        block_type, _ = block_info
        if block_type == "hollow":
            draw_rectangle_block({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [1,1,1])
        elif block_type == "solid":
            draw_rectangle_block_filled({"x1": coordinate[0], "y1": coordinate[1], 'width': 50, 'height': 20}, [1, 1, 1])

    # draw bat
    draw_rectangle_block(dx_bat, [1,1,1])

    # draw ball
    midpoint_circle(dx_ball_radius, [1,1,1], dx_ball_center)

    glutSwapBuffers()

glutInit()

glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutMainLoop()