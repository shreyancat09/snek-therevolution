import pygame
import random

print("Starting Snek Game...")
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FRAME_RATE = 60

# Color Definitions
COLOR_BG = (20, 24, 33)
COLOR_SNEK = (0, 230, 120)
COLOR_FOOD = (255, 60, 90)

# Window Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snek Revolution - Alpha v0.3")
clock = pygame.time.Clock()

# Snake Player Setup
snek_body = [(400, 300), (380, 300), (360, 300)]  # Start with 3 segments
snek_dir_x = GRID_SIZE
snek_dir_y = 0

# Food Spawning Logic
def spawn_food():
    fx = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    fy = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    return (fx, fy)

food_pos = spawn_food()

# Movement timer
move_delay = 120
last_move_time = pygame.time.get_ticks()

# Main Game Loop
is_running = True
while is_running:
    current_time = pygame.time.get_ticks()

    # 1. Event / Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snek_dir_y == 0:
                snek_dir_x = 0
                snek_dir_y = -GRID_SIZE
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snek_dir_y == 0:
                snek_dir_x = 0
                snek_dir_y = GRID_SIZE
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snek_dir_x == 0:
                snek_dir_x = -GRID_SIZE
                snek_dir_y = 0
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snek_dir_x == 0:
                snek_dir_x = GRID_SIZE
                snek_dir_y = 0

    # 2. Movement & Growth Logic
    if current_time - last_move_time >= move_delay:
        head_x, head_y = snek_body[0]
        new_head = (head_x + snek_dir_x, head_y + snek_dir_y)
        
        snek_body.insert(0, new_head)
        
        # Check if eating food
        if new_head == food_pos:
            food_pos = spawn_food()
        else:
            snek_body.pop()  # Remove tail if not eating

        last_move_time = current_time

    # 3. Render / Draw
    screen.fill(COLOR_BG)
    
    # Draw Food
    pygame.draw.rect(screen, COLOR_FOOD, (food_pos[0], food_pos[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=6)

    # Draw Snek Body
    for segment in snek_body:
        pygame.draw.rect(screen, COLOR_SNEK, (segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=4)

    # Update Display
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
