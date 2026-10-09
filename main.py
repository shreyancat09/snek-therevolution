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

# Font Setup
main_font = pygame.font.SysFont("Arial", 28, bold=True)

# Main Game Loop
is_running = True
while is_running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # 2. Render / Draw
    screen.fill(COLOR_BG)
    
    # Simple setup indicator
    title_surface = main_font.render("Snek Revolution - Press X to Close", True, COLOR_TEXT)
    screen.blit(title_surface, (50, 50))

    # Update Display
    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit()
