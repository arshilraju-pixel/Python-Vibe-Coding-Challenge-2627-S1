"""
HELLO KITTY: SWEET SHOP RUSH
A cute, pastel arcade game made with Python + Pygame.

Run:
    pip install pygame
    python hello_kitty_arcade.py

Controls:
    Left / Right arrows or A / D : Move
    P                         : Pause / resume
    Enter                     : Start / restart
    Esc                       : Quit
"""

import math
import random
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 650
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello Kitty: Sweet Shop Rush")
clock = pygame.time.Clock()

# Pastel arcade palette
PINK = (255, 184, 208)
LIGHT_PINK = (255, 224, 235)
PALE = (255, 246, 249)
HOT_PINK = (242, 92, 151)
DARK_PINK = (177, 64, 112)
WHITE = (255, 255, 255)
CREAM = (255, 244, 214)
BROWN = (103, 67, 68)
RED = (239, 91, 112)
MINT = (151, 222, 194)
PURPLE = (190, 165, 231)
GOLD = (255, 211, 104)

FONT = pygame.font.SysFont("arialrounded", 24, bold=True)
SMALL = pygame.font.SysFont("arialrounded", 17, bold=True)
BIG = pygame.font.SysFont("arialrounded", 54, bold=True)
TITLE = pygame.font.SysFont("arialrounded", 64, bold=True)

# Decorative background stars
stars = [(random.randrange(WIDTH), random.randrange(HEIGHT),
          random.uniform(0.7, 1.8), random.random() * math.tau)
         for _ in range(65)]


def draw_text(surface, text, font, color, center):
    image = font.render(text, True, color)
    surface.blit(image, image.get_rect(center=center))


def rounded_panel(surface, rect, color, radius=22, border=None, width=3):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width, border_radius=radius)


def draw_star(surface, x, y, size, color):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size * 0.42
        points.append((x + math.cos(angle) * r, y + math.sin(angle) * r))
    pygame.draw.polygon(surface, color, points)


def draw_background():
    screen.fill(PALE)
    # Soft horizontal pink bands
    for y in range(0, HEIGHT, 100):
        pygame.draw.rect(screen, (255, 239, 245), (0, y, WIDTH, 50))
    for x, y, size, phase in stars:
        twinkle = 0.65 + 0.35 * math.sin(pygame.time.get_ticks() / 500 + phase)
        draw_star(screen, x, y, max(2, int(size * 4 * twinkle)), (255, 198, 218))
    # Bottom checker-like arcade floor
    pygame.draw.rect(screen, (255, 213, 228), (0, HEIGHT - 22, WIDTH, 22))
    for x in range(0, WIDTH, 44):
        pygame.draw.rect(screen, (255, 190, 211), (x, HEIGHT - 22, 22, 22))


def draw_kitty(surface, cx, cy, scale=1.0):
    """Draw an original, simple Hello Kitty-inspired cat mascot."""
    def s(v):
        return int(v * scale)

    # Ears behind head
    pygame.draw.polygon(surface, WHITE, [
        (cx - s(39), cy - s(22)), (cx - s(49), cy - s(60)),
        (cx - s(13), cy - s(43))])
    pygame.draw.polygon(surface, WHITE, [
        (cx + s(39), cy - s(22)), (cx + s(49), cy - s(60)),
        (cx + s(13), cy - s(43))])
    pygame.draw.polygon(surface, PINK, [
        (cx - s(39), cy - s(32)), (cx - s(43), cy - s(51)),
        (cx - s(25), cy - s(42))])
    pygame.draw.polygon(surface, PINK, [
        (cx + s(39), cy - s(32)), (cx + s(43), cy - s(51)),
        (cx + s(25), cy - s(42))])
# Head
    pygame.draw.ellipse(surface, WHITE,
                       (cx - s(52), cy - s(42), s(104), s(82)))
    pygame.draw.ellipse(surface, DARK_PINK,
                       (cx - s(52), cy - s(42), s(104), s(82)), max(1, s(2)))

    # Eyes and nose
    pygame.draw.ellipse(surface, BROWN,
                       (cx - s(26), cy - s(5), s(7), s(11)))
    pygame.draw.ellipse(surface, BROWN,
                       (cx + s(19), cy - s(5), s(7), s(11)))
    pygame.draw.ellipse(surface, GOLD,
                       (cx - s(5), cy + s(8), s(10), s(7)))

    # Whiskers
    for side in (-1, 1):
        for offset in (-8, 0, 8):
            start_x = cx + side * s(35)
            end_x = cx + side * s(51)
            yy = cy + s(offset)
            pygame.draw.line(surface, BROWN, (start_x, yy), (end_x, yy - s(3)), max(1, s(2)))

    # Signature bow on upper-right ear
    bow_x, bow_y = cx + s(38), cy - s(39)
    pygame.draw.circle(surface, HOT_PINK, (bow_x - s(9), bow_y), s(10))
    pygame.draw.circle(surface, HOT_PINK, (bow_x + s(9), bow_y), s(10))
    pygame.draw.circle(surface, RED, (bow_x, bow_y), s(5))
    pygame.draw.circle(surface, DARK_PINK, (bow_x, bow_y), s(5), max(1, s(1)))


def draw_treat(surface, treat):
    x, y = int(treat["x"]), int(treat["y"])
    kind = treat["kind"]
    if kind == "strawberry":
        pygame.draw.circle(surface, RED, (x, y - 3), 13)
        pygame.draw.polygon(surface, RED, [(x - 12, y), (x + 12, y), (x, y + 17)])
        pygame.draw.polygon(surface, MINT, [(x - 8, y - 14), (x, y - 21), (x + 1, y - 12)])
        pygame.draw.polygon(surface, MINT, [(x + 1, y - 13), (x + 11, y - 16), (x + 5, y - 7)])
        for dx, dy in [(-5, -2), (4, 2), (-1, 8), (6, -7)]:
            pygame.draw.circle(surface, GOLD, (x + dx, y + dy), 2)
    elif kind == "cookie":
        pygame.draw.circle(surface, (211, 153, 105), (x, y), 15)
        pygame.draw.circle(surface, (245, 197, 143), (x, y), 12)
        for dx, dy in [(-5, -4), (5, 2), (-2, 7), (6, -7)]:
            pygame.draw.circle(surface, BROWN, (x + dx, y + dy), 2)
    elif kind == "candy":
        pygame.draw.circle(surface, PURPLE, (x, y), 12)
        pygame.draw.polygon(surface, PURPLE, [(x - 10, y - 7), (x - 21, y - 13), (x - 20, y + 8), (x - 10, y + 7)])
        pygame.draw.polygon(surface, PURPLE, [(x + 10, y - 7), (x + 21, y - 13), (x + 20, y + 8), (x + 10, y + 7)])
        pygame.draw.circle(surface, WHITE, (x - 3, y - 3), 3)
    else:  # silly little sour lemon: avoid it!
        pygame.draw.circle(surface, (188, 211, 91), (x, y), 14)
        pygame.draw.ellipse(surface, (220, 236, 139), (x - 8, y - 7, 16, 13))
        pygame.draw.line(surface, (102, 146, 91), (x - 3, y - 12), (x + 5, y - 18), 3)

class Game:
    def __init__(self):
        self.best = 0
        self.state = "menu"
        self.reset()

    def reset(self):
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 100
        self.player_speed = 7
        self.treats = []
        self.spawn_timer = 0
        self.score = 0
        self.lives = 3
        self.level = 1
        self.elapsed = 0
        self.invulnerable = 0
        self.state = "playing"

    def spawn_treat(self):
        kind = random.choices(
            ["strawberry", "cookie", "candy", "lemon"],
            weights=[36, 30, 24, 10], k=1
        )[0]
        self.treats.append({
            "x": random.randint(45, WIDTH - 45),
            "y": -30,
            "kind": kind,
            "speed": random.uniform(2.5, 4.0) + self.level * 0.45
        })

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed
        self.player_x = max(62, min(WIDTH - 62, self.player_x))

        self.elapsed += 1
        self.level = 1 + self.score // 120
        if self.invulnerable > 0:
            self.invulnerable -= 1

        self.spawn_timer += 1
        spawn_every = max(22, 54 - self.level * 3)
        if self.spawn_timer >= spawn_every:
            self.spawn_timer = 0
            self.spawn_treat()

        basket_rect = pygame.Rect(self.player_x - 48, self.player_y + 20, 96, 34)
        for treat in self.treats[:]:
            treat["y"] += treat["speed"]
            treat_rect = pygame.Rect(treat["x"] - 15, treat["y"] - 15, 30, 30)

            if basket_rect.colliderect(treat_rect):
                self.treats.remove(treat)
                if treat["kind"] == "lemon":
                    if self.invulnerable == 0:
                        self.lives -= 1
                        self.invulnerable = 75
                else:
                    points = {"strawberry": 15, "cookie": 10, "candy": 20}[treat["kind"]]
                    self.score += points
                continue

            if treat["y"] > HEIGHT + 25:
                self.treats.remove(treat)

        if self.lives <= 0:
            self.best = max(self.best, self.score)
            self.state = "gameover"

    def draw_hud(self):
        rounded_panel(screen, (18, 16, 864, 62), (255, 226, 237), 20, (255, 183, 208), 2)
        draw_text(screen, f"SCORE  {self.score}", FONT, DARK_PINK, (135, 47))
        draw_text(screen, f"LEVEL  {self.level}", FONT, DARK_PINK, (450, 47))
        draw_text(screen, f"LIVES  {'♥ ' * self.lives}", FONT, HOT_PINK, (760, 47))

    def draw(self):
        draw_background()

        if self.state == "menu":
            rounded_panel(screen, (125, 95, 650, 455), (255, 232, 241), 35, (255, 170, 202), 5)
            draw_star(screen, 190, 160, 17, GOLD)
            draw_star(screen, 710, 175, 17, GOLD)
            draw_kitty(screen, WIDTH // 2, 280, 1.55)
            draw_text(screen, "SWEET SHOP RUSH", TITLE, DARK_PINK, (450, 390))
            draw_text(screen, "Catch the treats. Dodge the sour lemons!", FONT, BROWN, (450, 438))
            rounded_panel(screen, (315, 475, 270, 54), HOT_PINK, 18, WHITE, 2)
            draw_text(screen, "PRESS ENTER TO PLAY", SMALL, WHITE, (450, 502))
            draw_text(screen, "← → or A / D to move   •   P to pause", SMALL, DARK_PINK, (450, 575))
            return

        self.draw_hud()

        # Little candy-shop awning
        for x in range(0, WIDTH, 90):
            pygame.draw.rect(screen, (255, 204, 220), (x, 92, 45, 13), border_radius=4)
            pygame.draw.rect(screen, WHITE, (x + 45, 92, 45, 13), border_radius=4)

            for treat in self.treats:
                draw_treat(screen, treat)

        # Basket
            basket_rect = pygame.Rect(self.player_x - 49, self.player_y + 20, 98, 35)
            pygame.draw.arc(screen, DARK_PINK, (self.player_x - 44, self.player_y + 5, 88, 42), math.pi, math.tau, 5)
            pygame.draw.rect(screen, (255, 179, 204), basket_rect, border_radius=10)
            pygame.draw.rect(screen, HOT_PINK, basket_rect, 3, border_radius=10)

            for x in range(self.player_x - 30, self.player_x + 31, 15):
                pygame.draw.line(screen, (255, 225, 235), (x, self.player_y + 23), (x, self.player_y + 52), 2)
            if self.invulnerable == 0 or (self.invulnerable // 6) % 2 == 0:
                draw_kitty(screen, self.player_x, self.player_y - 7, 0.72)

            if self.state == "paused":
                self.overlay("PAUSED", "Press P to continue")
            elif self.state == "gameover":
                self.overlay("GAME OVER!", f"Final score: {self.score}     Best: {self.best}",
                             "Press ENTER to play again")

        def overlay(self, heading, subtitle, extra=None):
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill((92, 48, 75, 115))
            screen.blit(shade, (0, 0))
            rounded_panel(screen, (185, 220, 530, 220), (255, 235, 243), 30, WHITE, 4)
            draw_text(screen, heading, BIG, DARK_PINK, (450, 280))
            draw_text(screen, subtitle, FONT, BROWN, (450, 335))
            if extra:
                draw_text(screen, extra, SMALL, HOT_PINK, (450, 390))


game = Game()
running = True

while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if game.state in ("menu", "gameover"):
                        game.reset()
                elif event.key == pygame.K_p:
                    if game.state == "playing":
                        game.state = "paused"
                    elif game.state == "paused":
                        game.state = "playing"

        game.update()
        game.draw()
        pygame.display.flip()

pygame.quit()
sys.exit()




