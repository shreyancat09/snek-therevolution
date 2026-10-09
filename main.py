import pygame
import random
import os

# Initialize Pygame modules
print("Starting Snek Game...")
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FRAME_RATE = 60

COLOR_BG = (20, 24, 33)
COLOR_SNEK = (0, 230, 120)
COLOR_TEXT = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snek Revolution - Alpha v0.4")
clock = pygame.time.Clock()

# Load Custom Coin Sprite
coin_img = None
if os.path.exists("imgs/gold.png"):
    coin_img = pygame.image.load("imgs/gold.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (GRID_SIZE, GRID_SIZE))

snek_body = [(400, 300), (380, 300), (360, 300)]
snek_dir_x = GRID_SIZE
snek_dir_y = 0
score = 0

def spawn_coin():
    fx = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    fy = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
    return (fx, fy)

coin_pos = spawn_coin()

is_game_over = False

move_delay = 120
last_move_time = pygame.time.get_ticks()

def reset_game():
    global snek_body, snek_dir_x, snek_dir_y, score, coin_pos, is_game_over
    snek_body = [(400, 300), (380, 300), (360, 300)]
    snek_dir_x = GRID_SIZE
    snek_dir_y = 0
    score = 0
    coin_pos = spawn_coin()
    is_game_over = False

is_running = True
while is_running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if is_game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
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


    if not is_game_over and (current_time - last_move_time >= move_delay):
        head_x, head_y = snek_body[0]
        new_head = (head_x + snek_dir_x, head_y + snek_dir_y)

    
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or 
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
            is_game_over = True

        elif new_head in snek_body:
            is_game_over = True

        else:
            snek_body.insert(0, new_head)

            if new_head == coin_pos:
                score += 10
                coin_pos = spawn_coin()
            else:
                snek_body.pop()

        last_move_time = current_time

   
    screen.fill(COLOR_BG)


    if coin_img:
        screen.blit(coin_img, coin_pos)
    else:
        pygame.draw.rect(screen, (255, 215, 0), (coin_pos[0], coin_pos[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=6)

    for segment in snek_body:
        pygame.draw.rect(screen, COLOR_SNEK, (segment[0], segment[1], GRID_SIZE - 2, GRID_SIZE - 2), border_radius=4)

    if is_game_over:
        font = pygame.font.SysFont("Arial", 36, bold=True)
        txt = font.render(f"GAME OVER - Score: {score} (Press 'R' to Restart)", True, COLOR_TEXT)
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(FRAME_RATE)

pygame.quit() 
