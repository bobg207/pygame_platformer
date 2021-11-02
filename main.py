import pygame
from settings import *
import os

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
        self.jump_height = int(self.height * .6)

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


class Walls():
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


pygame.init()

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Game Title")

clock = pygame.time.Clock()
player = Player(screen, BLUE,
                WALL_BRICK_WIDTH * 2,
                DISPLAY_HEIGHT - WALL_BRICK_HEIGHT - PLAYER_HEIGHT,
                PLAYER_WIDTH, PLAYER_HEIGHT)

wall_blocks = []
for row in range(len(LAYOUT)):
    y_loc = row * WALL_BRICK_HEIGHT
    for col in range(len(LAYOUT[0])):
        x_loc = col * WALL_BRICK_WIDTH
        if LAYOUT[row][col] == '1':
            brick = Walls(screen, RED, x_loc, y_loc, WALL_BRICK_WIDTH, WALL_BRICK_HEIGHT)
            wall_blocks.append(brick)

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for block in wall_blocks:
        block.make_walls()
    player.control_player()

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
