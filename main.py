import pygame

# Initialize Pygame modules
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_RATE = 60

# Color Definitions
COLOR_BG = (20, 24, 33)
COLOR_TEXT = (240, 240, 240)

# Window Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snek Revolution - Alpha v0.1")
clock = pygame.time.Clock()

# Snake Player Setup
snek_x = 400
snek_y = 300
snek_dir_x = GRID_SIZE
snek_dir_y = 0

# Movement timer to control snake speed without freezing frame rate
move_delay = 120  # milliseconds between steps
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
            # Change direction (prevents instant 180-degree reverse)
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

    # 2. Movement Logic
    if current_time - last_move_time >= move_delay:
        snek_x += snek_dir_x
        snek_y += snek_dir_y
        last_move_time = current_time

    # 3. Render / Draw
    screen.fill(COLOR_BG)
    
    # Draw Snek Head
    pygame.draw.rect(screen, COLOR_SNEK, (snek_x, snek_y, GRID_SIZE - 2, GRID_SIZE - 2), border_radius=4)

    # Update Display
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
