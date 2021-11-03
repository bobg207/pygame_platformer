import pygame
from settings import *
import os
import random

win_x = 50
win_y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{win_x},{win_y}"


class Player:
    def __init__(self, display, color, x, y, width, height):
        self.display = display
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velo = 5
        self.x_velo = 0
        self.y_velo = 3
        self.jumping = False
        self.falling = False
        self.y_counter = 0
        self.jump_height = self.height

    def draw_player(self):
        pygame.draw.rect(self.display, self.color,
                         (self.x, self.y, self.width, self.height))

    def player_keys(self):
        keys = pygame.key.get_pressed()

        # set x_velo base on key press
        if keys[pygame.K_LEFT]:
            self.x_velo = -1 * self.velo
        elif keys[pygame.K_RIGHT]:
            self.x_velo = self.velo
        else:
            self.x_velo = 0

        # set jump state on Space press
        if keys[pygame.K_SPACE] and self.jumping is False and self.falling is False:
            self.y_counter = 0
            self.jumping = True

    def move_player(self):
        self.x += self.x_velo

        # player movement is jumping, going up
        if self.jumping:
            self.y_counter += 1
            self.y -= self.y_velo

            if self.y_counter >= self.jump_height:
                self.jumping = False
                self.falling = True

        # player movement is falling, going down
        if self.falling:
            if self.y + self.height == DISPLAY_HEIGHT - WALL_BRICK_HEIGHT:
                self.y = DISPLAY_HEIGHT - WALL_BRICK_HEIGHT - self.height
                self.falling = False
            else:
                self.y += self.y_velo

    def on_platform(self, other):
        # for head bump
        if self.y <= other.y + other.height and \
                (other.x <= self.x + self.width <= other.x + other.width or \
                 other.x <= self.x <= other.x + other.width):
            self.jumping = False
            self.falling = True
        # front or back
        if self.x + self.width >= other.x and \
                (self.y <= other.y + other.height and
                 self.y + self.height >= other.y):
            self.x_velo = 0


    def is_collided(self, other):
        if (self.x <= other.x <= self.x + self.width or other.x <= self.x <= other.x + other.width) and \
                (self.y + self.height >= other.y >= self.y):
            return True

    def control_player(self):
        self.player_keys()
        self.move_player()
        self.draw_player()


class Ball:
    def __init__(self, display, color, x, y, width, height):
        self.display = display
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_velo = random.randint(1, 4)

    def make_ball(self):
        pygame.draw.circle(self.display, self.color,
                           (self.x, self.y), self.width)

    def update(self):
        self.x -= self.x_velo

        if self.x < -1 * self.width:
            self.x = random.randint(DISPLAY_WIDTH, DISPLAY_WIDTH + 50)


class Walls:
    def __init__(self, display, color, x, y, width, height):
        self.display = display
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def make_walls(self):
        pygame.draw.rect(self.display, self.color,
                         (self.x, self.y, self.width, self.height))


class Platform:
    def __init__(self, display, color, x, y, width, height):
        self.display = display
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def make_platform(self):
        pygame.draw.rect(self.display, self.color,
                         (self.x, self.y, self.width, self.height))


pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Game Title")

clock = pygame.time.Clock()
player = Player(screen, BLUE,
                WALL_BRICK_WIDTH * 2,
                DISPLAY_HEIGHT - WALL_BRICK_HEIGHT - PLAYER_HEIGHT,
                PLAYER_WIDTH, PLAYER_HEIGHT)

enemies = []
for i in range(5):
    ball_height = 20
    rand_x = random.randint(DISPLAY_WIDTH, DISPLAY_WIDTH + 50)
    y_loc = DISPLAY_HEIGHT - WALL_BRICK_HEIGHT - ball_height
    ball = Ball(screen, BLUE, rand_x, y_loc, ball_height, ball_height)
    enemies.append(ball)

wall_blocks = []
platforms = []
for row in range(len(LAYOUT)):
    y_loc = row * WALL_BRICK_HEIGHT
    for col in range(len(LAYOUT[0])):
        x_loc = col * WALL_BRICK_WIDTH
        if LAYOUT[row][col] == '1':
            brick = Walls(screen, RED, x_loc, y_loc, WALL_BRICK_WIDTH, WALL_BRICK_HEIGHT)
            wall_blocks.append(brick)
        elif LAYOUT[row][col] == '2':
            platf = Platform(screen, GREEN, x_loc, y_loc, WALL_BRICK_WIDTH, 20)
            platforms.append(platf)

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for block in wall_blocks:
        block.make_walls()

    for enemy in enemies:
        enemy.make_ball()
        enemy.update()

        # if player.is_collided(enemy):
        #     running = False

    for platform in platforms:
        platform.make_platform()
        player.on_platform(platform)

    player.control_player()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
