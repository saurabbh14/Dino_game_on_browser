import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 800, 300
WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (34, 177, 76), (255, 0, 0)

class Dino:
    def __init__(self):
        self.width, self.height = 40, 60
        self.x = 50
        self.y = HEIGHT - self.height - 30
        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 1
        self.jump_speed = -15

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y += self.vel_y
        self.vel_y += self.gravity
        if self.y >= HEIGHT - self.height - 30:
            self.y = HEIGHT - self.height - 30
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_speed
            self.is_jumping = True

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.get_rect())


class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.x = WIDTH
        self.y = HEIGHT - self.height - 30
        self.speed = 7

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_off_screen(self):
        return self.x + self.width < 0


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dino Clone OOP")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.dino = Dino()
        self.obstacles = []
        self.running = True
        self.game_over = False
        self.score = 0
        self.FPS = 60
        self.start_time = pygame.time.get_ticks()
        self.obstacle_timer = 0
        self.spawn_delay = random.randint(60, 180)

    def reset(self):
        self.dino = Dino()
        self.obstacles.clear()
        self.score = 0
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.obstacle_timer = 0
        self.FPS = 60

    def spawn_obstacle(self):
        self.obstacles.append(Obstacle())
        self.spawn_delay = random.randint(60, 180)
        self.obstacle_timer = 0

    def update(self):
        if not self.game_over:
            self.dino.update()
            self.obstacle_timer += 1

            if self.obstacle_timer > self.spawn_delay:
                self.spawn_obstacle()

            for obstacle in self.obstacles[:]:
                obstacle.update()
                if obstacle.get_rect().colliderect(self.dino.get_rect()):
                    self.game_over = True
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
                    self.score += 1
                    self.FPS = min(self.FPS + 1, 120)

    def draw(self):
        self.screen.fill(WHITE)
        self.dino.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f"Time: {elapsed}s", True, BLACK)
        self.screen.blit(time_text, (10, 40))

        if self.game_over:
            msg = self.font.render("Game Over! Press SPACE to restart", True, RED)
            self.screen.blit(msg, (WIDTH // 2 - 200, HEIGHT // 2))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.dino.jump()

    def wait_for_start(self):
        waiting = True
        while waiting:
            self.screen.fill(WHITE)
            msg = self.font.render("Press SPACE to start the game", True, BLACK)
            self.screen.blit(msg, (WIDTH // 2 - 200, HEIGHT // 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def run(self):
        self.wait_for_start()
        while self.running:
            self.clock.tick(self.FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
