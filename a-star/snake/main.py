import pygame.freetype
import sys
import time
from snake import *

# Colour definitions for drawing
# https://www.colorhexa.com/
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the dimensions of the grid
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Directions - used to find the neighbours of a node
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

FPS = 10

# Initialise Pygame - no pygame function can be called before this function is called
pygame.init()

# Initialise pygame specific values
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("A* Pathfinding Snake")
clock = pygame.time.Clock()


def print_results(font, size):
    # print to the console
    # https://datagy.io/python-concatenate-string-int/
    white_snake_score = "white snake: " + str(snake_one.score)
    yellow_snake_score = "yellow snake: " + str(snake_two.score)
    print(white_snake_score)
    print(yellow_snake_score)

    global screen

    # print to the GUI
    # https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
    # creating font object, create text_surface, and then blit the text_surface to the screen
    GAME_FONT = pygame.freetype.Font("FiraSans-Book.ttf", 48)
    ws_text_surface, rect = GAME_FONT.render(white_snake_score, RED)
    ys_text_surface, rect = GAME_FONT.render(yellow_snake_score, RED)
    screen.blit(ws_text_surface, (100, 150))
    screen.blit(ys_text_surface, (100, 350))
    pygame.display.flip()
    # wait for 2 seconds
    time.sleep(2)


snake_one = Snake(2, WHITE, BLUE)
snake_two = Snake(4, YELLOW, GREEN)
food = Food()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the Snake
    snake_one.move(food, snake_one, snake_two)
    snake_two.move(food, snake_one, snake_two)

    # Check for collision with Food
    if snake_one.body[0] == food.position:
        food.position = food.generate_position(snake_one, snake_two)
        snake_one.score += 10
        snake_one.grow = True

    if snake_two.body[0] == food.position:
        food.position = food.generate_position(snake_one, snake_two)
        snake_two.score += 10
        snake_two.grow = True

    # Check for snake collision with itself
    if snake_one.is_colliding():
        snake_one.dead = True

    if snake_two.is_colliding():
        snake_two.dead = True

    if snake_on_snake_collision(snake_one, snake_two):
        snake_one.dead = True

    if snake_on_snake_collision(snake_two, snake_one):
        snake_two.dead = True

    if snake_one.dead and snake_two.dead:
        print_results("FiraSans-Book.ttf", 24)
        running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the Snake and Food
    snake_one.draw(screen)
    snake_two.draw(screen)
    food.draw(screen, RED)

    # Update the display
    pygame.display.update()

    # Limit the framerate
    clock.tick(FPS)


# Close the program safely
pygame.quit()
sys.exit()
