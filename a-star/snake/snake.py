import random
import pygame
from a_star import *


class Snake:
    # div = division. Used to set the start position of the Snake in a dynamic way. Allows multiple snakes to be created
    # not dependent on screen-resolution
    def __init__(self, div, b_colour, h_colour):
        self.body = [(GRID_WIDTH // div, GRID_HEIGHT // div)]
        self.direction = random.choice(["up", "down", "left", "right"])
        self.grow = False
        self.dead = False
        self.body_colour = b_colour
        self.head_colour = h_colour
        self.score = 0

    def move(self, active_food, first_snake, second_snake):
        # Get the current position of the snake's head
        head = self.body[0]

        # Call the a_star() function to get the path from the snake's head to the food
        path = a_star(head, active_food.position, first_snake, second_snake)

        # If the path is not empty, get the next position and set the snake's position == to it.
        if path:
            # Get the next position of the snake's head from the path
            next_position = path[1]

            # Determine the direction of the snake's next move
            x_diff = next_position[0] - head[0]
            y_diff = next_position[1] - head[1]
            if x_diff == -1:
                self.direction = "left"
            elif x_diff == 1:
                self.direction = "right"
            elif y_diff == -1:
                self.direction = "up"
            elif y_diff == 1:
                self.direction = "down"

        # Move the snake to the next position
        if self.direction == "up":
            head = (head[0], head[1] - 1)
        elif self.direction == "down":
            head = (head[0], head[1] + 1)
        elif self.direction == "left":
            head = (head[0] - 1, head[1])
        elif self.direction == "right":
            head = (head[0] + 1, head[1])

        if head == active_food.position:
            self.grow = True

        self.body.insert(0, head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self, window):
        for i in range(len(self.body)):
            x, y = self.body[i]
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(window, self.body_colour, rect)
            if i == 0:
                pygame.draw.rect(window, self.head_colour, rect)

    def is_colliding(self):
        if self.body[0][0] < 0 or self.body[0][0] >= GRID_WIDTH:
            return True
        if self.body[0][1] < 0 or self.body[0][1] >= GRID_HEIGHT:
            return True
        for i in range(1, len(self.body)):
            if self.body[0] == self.body[i]:
                return True
        return False


def snake_on_snake_collision(dead_snake, hit_snake):
    for i in range(1, len(hit_snake.body)):
        if dead_snake.body[0] == hit_snake.body[i]:
            return True


# Define the Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Get a random position in the window and set a x and y co-ordinate. As long as the snake's body is not inside of
    # those co-ordinates, generate a new position, else repeat until a free space is found.
    def generate_position(self, first_snake, second_snake):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in first_snake.body:
                if (x, y) not in second_snake.body:
                    return x, y

    def draw(self, window, food_colour):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(window, food_colour, rect)
