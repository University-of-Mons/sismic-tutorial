import pygame
import sys
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
import threading
import time
import os
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Define_statechart.Car import Car
from Define_statechart.FrontCar import FrontCar


pygame.init()

# Window set up
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cruise Control simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)

image_directory = "Interface_to_external_components/img"
# Load images
steering_wheel_image = pygame.image.load(image_directory+'/volant.png')
accel_pedal_image = pygame.image.load(image_directory+'/accelerateur.png')
brake_pedal_image = pygame.image.load(image_directory+'/frein.png')
icon_CC_on = pygame.image.load(image_directory+'/CC_on.png')
icon_CC_activated = pygame.image.load(image_directory+'/CC_activated.png')
engine_off_image = pygame.image.load(image_directory+'/engine_off.png')
engine_on_image = pygame.image.load(image_directory+'/engine_on.png')
dist_button_image = pygame.image.load(image_directory+'/dist.png')
accel_pressed_image = pygame.image.load(image_directory+'/accelerateur_pressed.png')
brake_pressed_image = pygame.image.load(image_directory+'/frein_pressed.png')
mode_button_image = pygame.image.load(image_directory+'/CC_mode.png')
CC_on_off_button_image = pygame.image.load(image_directory+'/CC_on_off.png')
background_image = pygame.image.load(image_directory+"/background.png")
front_car_image = pygame.image.load(image_directory+"/front_car.png")
tree_image = pygame.image.load(image_directory+"/tree.png")

# Resize images
steering_wheel_image = pygame.transform.scale(steering_wheel_image, (350, 350))
accel_pedal_image = pygame.transform.scale(accel_pedal_image, (60, 140))
brake_pedal_image = pygame.transform.scale(brake_pedal_image, (60, 140))
icon_CC_activated = pygame.transform.scale(icon_CC_activated, (30, 30))
icon_CC_on = pygame.transform.scale(icon_CC_on, (30, 30))
engine_off_image = pygame.transform.scale(engine_off_image, (80, 80))
engine_on_image = pygame.transform.scale(engine_on_image, (80, 80))
dist_button_image = pygame.transform.scale(dist_button_image, (50, 30))
accel_pressed_image = pygame.transform.scale(accel_pressed_image, (60, 140))
brake_pressed_image = pygame.transform.scale(brake_pressed_image, (60, 140))
mode_button_image = pygame.transform.scale(mode_button_image, (50, 50))
CC_on_off_button_image = pygame.transform.scale(CC_on_off_button_image, (50, 50))
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH,WINDOW_HEIGHT))



# Relative positions
steering_wheel_pos = (WINDOW_WIDTH // 2 - steering_wheel_image.get_width() // 2, WINDOW_HEIGHT // 3)
accel_pedal_pos = (WINDOW_WIDTH // 2 + 150, 650)
brake_pedal_pos = (WINDOW_WIDTH // 2 + 50, 650)
dashboard_width, dashboard_height = 180, 90
dashboard_pos = (steering_wheel_pos[0] + steering_wheel_image.get_width() // 2 - dashboard_width // 2, steering_wheel_pos[1] + steering_wheel_image.get_height() // 2 - dashboard_height * 1.5)
engine_button_pos = (steering_wheel_pos[0] + steering_wheel_image.get_width() + 20, steering_wheel_pos[1] + steering_wheel_image.get_height() // 2 - 30)
icon_cruise_pos_in_dashboard = (dashboard_pos[0] + dashboard_width // 2 - icon_CC_activated.get_width() // 2 - 2, dashboard_pos[1] + dashboard_height - icon_CC_activated.get_height() - 10)
speed_text_pos = (dashboard_pos[0] + dashboard_width // 2 - 32, dashboard_pos[1] + 4)

original_tree_width, original_tree_height = (60,70)


stop_y = 320
horizon_y = 115

## Trees
trees = []
nb_trees = 20
spacing = (stop_y - horizon_y) / nb_trees
for side in [-1, 1]:
    for i in range(nb_trees):
        trees.append({'side': side, 'y': horizon_y + i * spacing, 'scale': 0.3})


# Font and sizes
font_path = "Interface_to_external_components/DejaVuSansMono.ttf"
font_large = pygame.font.Font(font_path, 36)
font_small = pygame.font.Font(font_path, 20)
font_tiny = pygame.font.Font(font_path, 12)
font_button = pygame.font.Font(font_path, 32)

# Pre-draw static interface (dashboard, steering wheel and buttons) into a surface
static_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
static_surface.blit(background_image, (0,0))

dashboard_rect = pygame.Rect(dashboard_pos[0] - 5, dashboard_pos[1] - 5, dashboard_width + 10, dashboard_height + 10)
pygame.draw.rect(static_surface, WHITE, dashboard_rect, border_radius=10)
pygame.draw.rect(static_surface, DARK_GRAY, (*dashboard_pos, dashboard_width, dashboard_height), border_radius=8)

static_surface.blit(steering_wheel_image, steering_wheel_pos)

### CC buttons

cc_grid_x, cc_grid_y = 50, 600 
cc_cell_width, cc_cell_height = 80, 60 
cc_cell_thickness = 5

# Draw vertical lines
pygame.draw.line(static_surface, GRAY, (cc_grid_x, cc_grid_y), (cc_grid_x, cc_grid_y + cc_cell_height * 2), cc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (cc_grid_x + cc_cell_width, cc_grid_y), (cc_grid_x + cc_cell_width, cc_grid_y + cc_cell_height * 2), cc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (cc_grid_x + cc_cell_width * 2, cc_grid_y), (cc_grid_x + cc_cell_width * 2, cc_grid_y + cc_cell_height * 2), cc_cell_thickness)

# Draw horizontal lines
pygame.draw.line(static_surface, GRAY, (cc_grid_x, cc_grid_y), (cc_grid_x + cc_cell_width * 2, cc_grid_y), cc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (cc_grid_x, cc_grid_y + cc_cell_height), (cc_grid_x + cc_cell_width * 2, cc_grid_y + cc_cell_height), cc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (cc_grid_x, cc_grid_y + cc_cell_height * 2), (cc_grid_x + cc_cell_width * 2, cc_grid_y + cc_cell_height * 2), cc_cell_thickness)


### ACC buttons

acc_grid_x, acc_grid_y = 50, 730
acc_cell_width, acc_cell_height = 60, 60
acc_cell_thickness = 5

# Draw vertical lines
pygame.draw.line(static_surface, GRAY, (acc_grid_x, acc_grid_y), (acc_grid_x, acc_grid_y + acc_cell_height), acc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (acc_grid_x + acc_cell_width, acc_grid_y), (acc_grid_x + acc_cell_width, acc_grid_y + acc_cell_height), acc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (acc_grid_x + acc_cell_width * 2, acc_grid_y), (acc_grid_x + acc_cell_width * 2, acc_grid_y + acc_cell_height), acc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (acc_grid_x + acc_cell_width * 3, acc_grid_y), (acc_grid_x + acc_cell_width * 3, acc_grid_y + acc_cell_height), acc_cell_thickness)

# Draw horizontal lines
pygame.draw.line(static_surface, GRAY, (acc_grid_x, acc_grid_y), (acc_grid_x + acc_cell_width * 3, acc_grid_y), acc_cell_thickness)
pygame.draw.line(static_surface, GRAY, (acc_grid_x, acc_grid_y + acc_cell_height), (acc_grid_x + acc_cell_width * 3, acc_grid_y + acc_cell_height), acc_cell_thickness)


res_pos = (cc_grid_x + 10, cc_grid_y + cc_cell_height + 10)
set_pos = (cc_grid_x + 10, cc_grid_y + 10)
mode_pos = (cc_grid_x + cc_cell_width*2 - 65, cc_grid_y + cc_cell_height + 6)
on_off_pos = (cc_grid_x + cc_cell_width * 2 - 65, cc_grid_y + 4)
dist_pos = (acc_grid_x + acc_cell_width + 5, acc_grid_y + 13)
minus_pos = (acc_grid_x + 20, acc_grid_y + 13)
plus_pos = (acc_grid_x + acc_cell_width*2 + 20, acc_grid_y + 13)


kmh_text = font_small.render("km/h", True, WHITE)
kmh_text_pos = (speed_text_pos[0] + 68, speed_text_pos[1] + 14)
static_surface.blit(kmh_text, (kmh_text_pos[0], kmh_text_pos[1]))

little_kmh = font_tiny.render("km/h", True, WHITE)
static_surface.blit(little_kmh, (dashboard_pos[0] + 9, dashboard_pos[1] + dashboard_height // 2 + 2))

res_text = font_button.render("RES", True, WHITE)
static_surface.blit(res_text, res_pos)

set_text = font_button.render("SET", True, WHITE)
static_surface.blit(set_text, set_pos)

minus_text = font_button.render("-", True, WHITE)
static_surface.blit(minus_text, minus_pos)

plus_text = font_button.render("+", True, WHITE)
static_surface.blit(plus_text, plus_pos)

static_surface.blit(CC_on_off_button_image, on_off_pos)

static_surface.blit(mode_button_image, mode_pos)

static_surface.blit(dist_button_image, dist_pos)


# Dictionary that keeps all the rectangles associated to the buttons
global buttons_rects
buttons_rects = {}

# TODO : Improve the rect for on_off and mode to fit the entire cell, and for SET + RES
buttons_rects["SET"] = pygame.Rect(set_pos[0], set_pos[1], set_text.get_width(), set_text.get_height())
buttons_rects["RES"] = pygame.Rect(res_pos[0], res_pos[1], res_text.get_width(), res_text.get_height())
buttons_rects["-"] = pygame.Rect(minus_pos[0], minus_pos[1], 40, 40)
buttons_rects["+"] = pygame.Rect(plus_pos[0], plus_pos[1], 40, 40)
buttons_rects["MODE"] = pygame.Rect(mode_pos[0], mode_pos[1], mode_button_image.get_width(), mode_button_image.get_height())
buttons_rects["ON/OFF"] = pygame.Rect(on_off_pos[0], on_off_pos[1], CC_on_off_button_image.get_width(), CC_on_off_button_image.get_height())
buttons_rects["DIST"] = pygame.Rect(dist_pos[0], dist_pos[1], 50, 30)
buttons_rects["ACCEL"] = pygame.Rect(accel_pedal_pos[0], accel_pedal_pos[1], 60, 140)
buttons_rects["BRAKE"] = pygame.Rect(brake_pedal_pos[0], brake_pedal_pos[1], 60, 140)
buttons_rects["ENGINE"] = pygame.Rect(engine_button_pos[0], engine_button_pos[1], 80, 80)

# Actions associated with buttons
def action_res(statechart):
    print("Action RES")
    statechart.queue("res_button_pressed")
    statechart.execute_once()

def action_set(statechart):
    print("Action SET")
    statechart.queue("set_button_pressed")
    statechart.execute_once()

def action_minus(statechart):
    print("Action - ")
    statechart.queue("minus_button_pressed")
    statechart.execute_once()

def action_plus(statechart):
    print("Action +")
    statechart.queue("plus_button_pressed")
    statechart.execute_once()

def action_mode(statechart):
    print("Action MODE")
    statechart.queue("mode_button_pressed")
    statechart.execute_once()

def action_on_off(statechart):
    print("Action ON/OFF")
    statechart.queue("on_off_button_pressed")
    statechart.execute_once()

def action_dist(statechart):
    print("Action DIST")
    statechart.queue("mode_button_pressed")
    statechart.execute_once()

def action_accel(statechart):
    print("Action ACCEL")
    statechart.queue("accelerate",accel=100)
    statechart.execute_once()

def action_brake(statechart):
    print("Action BRAKE")
    statechart.queue("brake", decel=100)
    statechart.execute_once()

def action_accel_released(statechart):
    print("ACCEL released")
    statechart.queue("stop_accelerate")
    statechart.execute_once()

def action_brake_released(statechart):
    print("BRAKE released")
    statechart.queue("stop_brake")
    statechart.execute_once()

def action_engine(statechart):
    global engine_on
    if statechart.context['car'].is_stationary():
        engine_on = not engine_on
        statechart.queue("engine_start_stop_button_pressed")
        statechart.execute_once()
        print("Engine is now", "ON" if engine_on else "OFF")
        
# Link the names with the funtions
button_actions = {
    "RES": action_res,
    "SET": action_set,
    "-": action_minus,
    "+": action_plus,
    "MODE": action_mode,
    "ON/OFF": action_on_off,
    "DIST": action_dist,
    "ACCEL": action_accel,
    "BRAKE": action_brake,
    "ENGINE": action_engine,
}


def draw_dynamic_buttons():
    # accel/brake
    global accel_pressed
    global brake_pressed

    if accel_pressed:
        window.blit(accel_pressed_image, accel_pedal_pos)
    else:
        window.blit(accel_pedal_image, accel_pedal_pos)

    if brake_pressed:
        window.blit(brake_pressed_image, brake_pedal_pos)
    else:
        window.blit(brake_pedal_image, brake_pedal_pos)

    # ENGINE
    engine_image = engine_on_image if engine_on else engine_off_image
    window.blit(engine_image, engine_button_pos)


def tick_thread():
    global inter
    global front_car
    while True:
        front_car.update_distance()
        inter.queue("tick")
        inter.execute()
        time.sleep(0.1)


statechart = import_from_yaml(filepath='Define_statechart/statechart_with_contracts.yaml')
car = Car()
front_car = FrontCar(10,250)
inter = Interpreter(statechart, initial_context={'car':car,'front_car':front_car})


thread = threading.Thread(target=tick_thread, daemon=True)
thread.start() 

# Instanciate property statecharts
property_dir = os.path.join(os.getcwd(), 'Define_property_statechart')
if os.path.exists(property_dir):
    for file_path in glob.glob(os.path.join(property_dir, "*property.yaml")):
        property_statechart = import_from_yaml(filepath=file_path)
        inter.bind_property_statechart(property_statechart)

# Initial step
inter.execute_once()

# States for displaying the buttons
engine_on = False
accel_pressed = False
brake_pressed = False

clock = pygame.time.Clock()
fps = 15

# Infinite loop for the display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # button press
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button_name, rect in buttons_rects.items():
                if rect.collidepoint(mouse_pos):
                    action = button_actions.get(button_name)
                    if action:
                        action(inter)

                    if button_name == "ACCEL":
                        accel_pressed = True
                    if button_name == "BRAKE":
                        brake_pressed = True

        # button release
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            if buttons_rects["ACCEL"].collidepoint(mouse_pos):
                action_accel_released(inter)
                accel_pressed = False
            elif buttons_rects["BRAKE"].collidepoint(mouse_pos):
                action_brake_released(inter)
                brake_pressed = False
    
    speed = car.get_speed()

    # Drawing static interface
    window.fill(BLACK)
    window.blit(static_surface, (0, 0))

    # Speed
    speed_text = font_large.render(f"{speed}", True, WHITE)
    window.blit(speed_text, (speed_text_pos[0], speed_text_pos[1]))

    # CC icons
    CC_activated = inter.configuration.__contains__("Activated")
    CC_on = inter.configuration.__contains__("On")
    if CC_activated:
        # CC_activated
        window.blit(icon_CC_activated, icon_cruise_pos_in_dashboard)
    elif CC_on:
        # CC_on
        window.blit(icon_CC_on, icon_cruise_pos_in_dashboard)

    # mem_speed
    mem_speed = inter.context['mem_speed']
    mem_speed_text = font_small.render(f"{mem_speed}", True, WHITE)
    window.blit(mem_speed_text, (dashboard_pos[0] + 6, dashboard_pos[1] + dashboard_height // 2 + 17))

    # Draw dynamic buttons
    draw_dynamic_buttons()

    # Trees
    center_x = WINDOW_WIDTH // 2
    spread = 1500 

    for tree in trees:
        speed_factor = car.get_speed() * 0.014
        tree['y'] += speed_factor

        t = (tree['y'] - horizon_y) / (stop_y - horizon_y)
        t = max(0, min(1, t))

        x = center_x + tree['side'] * (5 + spread * t)
        scale = 0.3 + 15 * (t ** 1.1)

        scaled_tree = pygame.transform.scale(tree_image, (
            int(original_tree_width * scale),
            int(original_tree_height * scale)
        ))

        tree_x = x - scaled_tree.get_width() // 2
        tree_y = tree['y']

        if tree['y'] >= horizon_y:
            if tree['y'] <= stop_y:
                window.blit(scaled_tree, (tree_x, tree_y))
            else:
                tree['y'] = tree['y'] - (stop_y - horizon_y)


    # Front car 
    distance = front_car.distance_to()

    if distance <= 280:
        scale = (280 - distance) / 400

        y_add = 60*scale
        y_pos = horizon_y  + 15 + y_add

        scaled_width = int(front_car_image.get_width() * scale)
        scaled_height = int(front_car_image.get_height() * scale)
        scaled_front_car = pygame.transform.scale(front_car_image, (scaled_width, scaled_height))

        x_pos = WINDOW_WIDTH // 2 - scaled_height // 2

        window.blit(scaled_front_car, (x_pos, y_pos - scaled_height // 2))


    # Update display
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
sys.exit()
