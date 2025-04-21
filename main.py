import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Dino settings
dino_width, dino_height = 40, 60
dino_x, dino_y = 50, HEIGHT - dino_height - 30
jump_speed = -15
gravity = 1

# Obstacle settings
obstacle_width = 20
obstacle_height = 40
obstacle_speed = 7
obstacle_timer = 0

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game variables
dino_vel_y = 0
is_jumping = False
obstacles = []

# Game loop
game_over = False
running = True
start_time = pygame.time.get_ticks()
while running:
    clock.tick(FPS)
    SCREEN.fill(WHITE)

    # Draw dino
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    pygame.draw.rect(SCREEN, BLACK, dino_rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                is_jumping = True
                dino_vel_y = jump_speed

            if event.key == pygame.K_SPACE and game_over:
                # Reset game state
                dino_y = HEIGHT - dino_height - 30
                dino_vel_y = 0
                is_jumping = False
                obstacles.clear()
                score = 0
                obstacle_timer = 0
                start_time = pygame.time.get_ticks()
                game_over = False
                FPS = 60

    # Handle jumping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        dino_vel_y = jump_speed
        is_jumping = True

    dino_y += dino_vel_y
    dino_vel_y += gravity

    if dino_y >= HEIGHT - dino_height - 30:
        dino_y = HEIGHT - dino_height - 30
        is_jumping = False



    # Spawn obstacles
    obstacle_timer += 1
    if obstacle_timer > random.randint(60, 180):
        obstacle_timer = 0
        new_obstacle = pygame.Rect(WIDTH, HEIGHT - obstacle_height - 30, obstacle_width, obstacle_height)
        obstacles.append(new_obstacle)
    if  not game_over:
        # Move and draw obstacles
        for obstacle in obstacles[:]:
            obstacle.x -= obstacle_speed
            pygame.draw.rect(SCREEN, GREEN, obstacle)

            # Collision check
            if dino_rect.colliderect(obstacle):
                game_over = True

            # Remove off-screen obstacles
            if obstacle.x + obstacle_width < 0:
                obstacles.remove(obstacle)
                score += 1
                FPS += 2


        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # in seconds
        time_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        SCREEN.blit(time_text, (10, 40))

    if game_over:
        over_text = font.render("Game Over! Press Space bar to restart", True, (255, 0, 0))
        SCREEN.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()