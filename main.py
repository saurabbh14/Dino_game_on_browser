import pygame
import random
import asyncio
import sys

class Dino:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.is_jumping = False
        self.jump_speed = -15

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_speed
            self.is_jumping = True

    def update(self, gravity):
        self.rect.y += self.vel_y
        self.vel_y += gravity

        # Ground collision
        if self.rect.y >= HEIGHT - self.rect.height - 30:
            self.rect.y = HEIGHT - self.rect.height - 30
            self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Obstacle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chrome Dino Clone")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.reset_game()

    def reset_game(self):
        self.dino = Dino(50, HEIGHT - 90, 40, 60)
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.start_time = pygame.time.get_ticks()
        self.fps = 60

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.dino.jump()

        return True

    def update(self):
        if not self.game_over:
            self.dino.update(GRAVITY)
            
            # Spawn obstacles
            self.obstacle_timer += 1
            if self.obstacle_timer > random.randint(60, 180):
                self.obstacle_timer = 0
                new_obstacle = Obstacle(WIDTH, HEIGHT - 70, 20, 40, 7)
                self.obstacles.append(new_obstacle)

            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.update()

                # Collision check
                if self.dino.rect.colliderect(obstacle.rect):
                    self.game_over = True

                # Remove off-screen obstacles and update score
                if obstacle.rect.right < 0:
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.fps += 2

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw game elements
        self.dino.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Draw score and time
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = font.render(f"Time: {elapsed_time}s", True, BLACK)
        self.screen.blit(time_text, (10, 40))

        if self.game_over:
            over_text = font.render("Game Over! Press Space bar to restart", True, (255, 0, 0))
            self.screen.blit(over_text, (WIDTH // 2 - 160, HEIGHT // 2))

        pygame.display.flip()

    async def game_loop(self):
        while True:
            if not self.handle_events():
                break

            self.update()
            self.draw()
            self.clock.tick(self.fps)
            
            # Required for Pygbag
            await asyncio.sleep(0)

# Game constants
WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
GRAVITY = 1

async def main():
    game = Game()
    await game.game_loop()
    pygame.quit()

if __name__ == '__main__':
    asyncio.run(main())