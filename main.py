import pygame
import random
import os

pygame.init()
pygame.mixer.init()

w, h = 800, 600
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snek Revolution")
clk = pygame.time.Clock()

grid = 20

bg_color = (20, 24, 33)
head_color = (0, 255, 180)
body_color = (0, 190, 100)
boost_color = (255, 200, 0)
txt_color = (255, 255, 255)
sub_txt = (150, 160, 180)
hazard_color = (220, 50, 50)
apple_color = (255, 215, 0)

coin_img = None
if os.path.exists("imgs/gold.png"):
    coin_img = pygame.image.load("imgs/gold.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (grid, grid))

head_img = None
if os.path.exists("imgs/head.png"):
    head_img = pygame.image.load("imgs/head.png").convert_alpha()
    head_img = pygame.transform.scale(head_img, (grid, grid))

sfx_coin = None
sfx_over = None
if os.path.exists("audio/coin.wav"):
    sfx_coin = pygame.mixer.Sound("audio/coin.wav")
if os.path.exists("audio/gameover.wav"):
    sfx_over = pygame.mixer.Sound("audio/gameover.wav")

best_score = 0
mode = "menu"  # menu, run, over

snake = [(400, 300), (380, 300), (360, 300)]
dx = grid
dy = 0
pts = 0
streak = 0
spd = 120

def get_pos():
    rx = random.randint(0, (w - grid) // grid) * grid
    ry = random.randint(0, (h - grid) // grid) * grid
    return (rx, ry)

coin_pos = get_pos()

# feATURE 1: random obstacles
hazards = [get_pos(), get_pos()]

# featuer 2: special apple 
bonus_pos = None
bonus_timer = 0

last_step = pygame.time.get_ticks()

def restart():
    global snake, dx, dy, pts, streak, spd, coin_pos, hazards, bonus_pos, mode
    snake = [(400, 300), (380, 300), (360, 300)]
    dx = grid
    dy = 0
    pts = 0
    streak = 0
    spd = 120
    coin_pos = get_pos()
    hazards = [get_pos(), get_pos()]
    bonus_pos = None
    mode = "run"

# fonts
f_big = pygame.font.SysFont("Arial", 40, bold=True)
f_med = pygame.font.SysFont("Arial", 22, bold=True)

done = False
while not done:
    now = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = True
        elif e.type == pygame.KEYDOWN:
            if mode == "menu":
                if e.key == pygame.K_SPACE:
                    restart()
            elif mode == "over":
                if e.key == pygame.K_r:
                    restart()
                elif e.key == pygame.K_SPACE:
                    mode = "menu"
            elif mode == "run":
                if (e.key in (pygame.K_UP, pygame.K_w)) and dy == 0:
                    dx, dy = 0, -grid
                elif (e.key in (pygame.K_DOWN, pygame.K_s)) and dy == 0:
                    dx, dy = 0, grid
                elif (e.key in (pygame.K_LEFT, pygame.K_a)) and dx == 0:
                    dx, dy = -grid, 0
                elif (e.key in (pygame.K_RIGHT, pygame.K_d)) and dx == 0:
                    dx, dy = grid, 0

    if mode == "run" and (now - last_step >= spd):
        head = (snake[0][0] + dx, snake[0][1] + dy)

        if (head[0] < 0 or head[0] >= w or head[1] < 0 or head[1] >= h or 
            head in snake or head in hazards):
            mode = "over"
            if sfx_over:
                sfx_over.play()
            if pts > best_score:
                best_score = pts
        else:
            snake.insert(0, head)
            
            if head == coin_pos:
                streak += 1
                pts += 10 * (1 + streak // 5)
                if spd > 60:
                    spd -= 2
                if sfx_coin:
                    sfx_coin.play()
                coin_pos = get_pos()

                if random.random() < 0.3 and bonus_pos is None:
                    bonus_pos = get_pos()
                    bonus_timer = now

            elif bonus_pos and head == bonus_pos:
                pts += 50
                spd = min(120, spd + 10)  # slows down speed temporarily
                bonus_pos = None
                if sfx_coin:
                    sfx_coin.play()

            else:
                snake.pop()

            if bonus_pos and (now - bonus_timer > 5000):
                bonus_pos = None

        last_step = now

    win.fill(bg_color)

    if mode == "menu":
        t1 = f_big.render("Snek Revolution by Shreyancat", True, head_color)
        t2 = f_med.render("Press SPACE to Start", True, txt_color)
        t3 = f_med.render(f"High Score: {best_score}", True, sub_txt)
        win.blit(t1, (w // 2 - t1.get_width() // 2, h // 2 - 60))
        win.blit(t2, (w // 2 - t2.get_width() // 2, h // 2 + 10))
        win.blit(t3, (w // 2 - t3.get_width() // 2, h // 2 + 50))

    elif mode in ("run", "over"):
        for hz in hazards:
            pygame.draw.rect(win, hazard_color, (hz[0], hz[1], grid - 2, grid - 2), border_radius=4)

        if bonus_pos:
            pygame.draw.circle(win, apple_color, (bonus_pos[0] + grid // 2, bonus_pos[1] + grid // 2), grid // 2 - 1)

        if coin_img:
            win.blit(coin_img, coin_pos)
        else:
            pygame.draw.rect(win, (255, 215, 0), (coin_pos[0], coin_pos[1], grid - 2, grid - 2), border_radius=6)

        for idx, seg in enumerate(snake):
            if idx == 0:
                if head_img:
                    win.blit(head_img, seg)
                else:
                    pygame.draw.rect(win, head_color, (seg[0], seg[1], grid - 2, grid - 2), border_radius=6)
            else:
                c = boost_color if streak >= 5 else body_color
                pygame.draw.rect(win, c, (seg[0], seg[1], grid - 2, grid - 2), border_radius=4)

        s_txt = f_med.render(f"Score: {pts}", True, txt_color)
        b_txt = f_med.render(f"Best: {best_score}", True, sub_txt)
        c_txt = f_med.render(f"Combo: x{1 + streak // 5}", True, boost_color)
        win.blit(s_txt, (20, 20))
        win.blit(b_txt, (20, 45))
        win.blit(c_txt, (w - 140, 20))

        if mode == "over":
            o_txt = f_big.render("GAME OVER", True, (255, 60, 90))
            r_txt = f_med.render("Press 'R' to Restart or SPACE for Menu", True, txt_color)
            win.blit(o_txt, (w // 2 - o_txt.get_width() // 2, h // 2 - 40))
            win.blit(r_txt, (w // 2 - r_txt.get_width() // 2, h // 2 + 10))

    pygame.display.flip()
    clk.tick(60)

pygame.quit()
