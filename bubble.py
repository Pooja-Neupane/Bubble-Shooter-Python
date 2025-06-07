import pygame
import random
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 600, 800
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OOP Bubble Shooter 🎯")

# Colors
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

class Bubble:
    def __init__(self, x, y, color, radius=20):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.vel_x = 0
        self.vel_y = 0
        self.fired = False
        self.stuck = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        if self.fired and not self.stuck:
            self.x += self.vel_x
            self.y += self.vel_y
            if self.x <= self.radius or self.x >= WIDTH - self.radius:
                self.vel_x *= -1

    def collide(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.hypot(dx, dy) <= self.radius * 2

class Grid:
    def __init__(self, rows=5, cols=8):
        self.bubbles = []
        self.init_grid(rows, cols)

    def init_grid(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                x = col * 70 + 50
                y = row * 70 + 50
                bubble = Bubble(x, y, random.choice(COLORS))
                bubble.stuck = True
                self.bubbles.append(bubble)

    def draw(self, surface):
        for bubble in self.bubbles:
            bubble.draw(surface)

    def check_collision_and_stick(self, bubble):
        for b in self.bubbles:
            if bubble.collide(b):
                bubble.stuck = True
                bubble.x = b.x
                bubble.y = b.y - 40
                self.bubbles.append(bubble)
                return True
        return False

class Shooter:
    def __init__(self):
        self.bubble = self.create_new_bubble()

    def create_new_bubble(self):
        return Bubble(WIDTH // 2, HEIGHT - 50, random.choice(COLORS))

    def aim_and_fire(self, mx, my):
        angle = math.atan2(my - self.bubble.y, mx - self.bubble.x)
        speed = 10
        self.bubble.vel_x = speed * math.cos(angle)
        self.bubble.vel_y = speed * math.sin(angle)
        self.bubble.fired = True

    def update(self):
        self.bubble.move()

    def draw(self, surface):
        self.bubble.draw(surface)

    def reset_if_stuck(self):
        if self.bubble.stuck or self.bubble.y <= 0:
            self.bubble = self.create_new_bubble()

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = Grid()
        self.shooter = Shooter()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.shooter.bubble.fired:
                mx, my = pygame.mouse.get_pos()
                self.shooter.aim_and_fire(mx, my)

    def update(self):
        self.shooter.update()
        if self.shooter.bubble.fired:
            if self.grid.check_collision_and_stick(self.shooter.bubble):
                self.shooter.reset_if_stuck()
            elif self.shooter.bubble.y <= 0:
                self.shooter.bubble.stuck = True
                self.grid.bubbles.append(self.shooter.bubble)
                self.shooter.reset_if_stuck()

    def draw(self):
        win.fill(WHITE)
        self.grid.draw(win)
        self.shooter.draw(win)
        pygame.display.update()

# Run the game
if __name__ == "__main__":
    Game().run()
