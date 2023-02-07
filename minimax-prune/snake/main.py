import pygame
import time
import random


def initialise_game():
    global score
    score = 0

    # Set game values
    # defining snake default position
    global snake_position
    snake_position = [100, 50]

    # defining first 4 blocks of snake
    # body
    global snake_body
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    # fruit position
    global pickup_position
    pickup_position = generate_pickup()
    global pickup_currently_exists
    pickup_currently_exists = True


# displaying Score function
def show_score(color, font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()

    # displaying text
    global window
    window.blit(score_surface, score_rect)


def generate_pickup():
    return [random.randrange(1, (WINDOW_X / 10)) * 10,
            random.randrange(1, (WINDOW_Y / 10)) * 10]


def move_snake(current_snake_position, move_dir):
    global direction
    if move_dir == 0:  # up
        current_snake_position[1] -= 10
        direction = "UP"
    if move_dir == 1:  # down
        current_snake_position[1] += 10
        direction = "DOWN"
    if move_dir == 2:  # left
        current_snake_position[0] -= 10
        direction = "LEFT"
    if move_dir == 3:  # right
        current_snake_position[0] += 10
        direction = "RIGHT"


def distance_snake_pickup(s_pos, p_pos):
    x_dist = s_pos[0] - p_pos[0]
    y_dist = s_pos[1] - p_pos[1]

    return [x_dist, y_dist]


def agent_min(gamestate, alpha, beta):
    return 0


def agent_max(gamestate, alpha, beta):
    return 0


def move_minmax(current_snake_position, current_pickup_position):
    global direction
    has_moved = False
    distance = distance_snake_pickup(current_snake_position, current_pickup_position)
    while not has_moved:
        print(direction)
        print(distance)
        if distance[1] > 0 and not direction == "DOWN":
            move_snake(current_snake_position, 0)
            has_moved = True
        elif distance[1] < 0 and not direction == "UP":
            move_snake(current_snake_position, 1)
            has_moved = True
        if distance[0] > 0 and not direction == "RIGHT":
            move_snake(current_snake_position, 2)
            has_moved = True
        elif distance[0] < 0 and not direction == "LEFT":
            move_snake(current_snake_position, 3)
            has_moved = True
    print(direction)


def move_randomly(current_snake_position):
    global direction
    has_moved = False
    while not has_moved:
        # grab a random direction
        move_dir = random.randint(0, 3)

        # stop immediate reverse direction
        if move_dir == 0 and direction == "DOWN":
            continue
        if move_dir == 1 and direction == "UP":
            continue
        if move_dir == 2 and direction == "RIGHT":
            continue
        if move_dir == 3 and direction == "LEFT":
            continue

        print(direction)
        print(move_dir)
        move_snake(current_snake_position, move_dir)
        has_moved = True


# game over function
def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('urw bookman', 42)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, BLACK)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (WINDOW_X / 4, WINDOW_Y / 4)

    # blit will draw the text on screen
    global window
    window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the
    # program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


# global const
WINDOW_X = 1280  # the window will be (1280, 720). This still must be set
WINDOW_Y = 720
# set the colours for the game. I have chosen black and white for ease of contrast
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

# Create global values
score = 0
snake_position = [0, 0]
snake_body = [[0, 0]]
snake_body_segment_size = 10
snake_speed = 60
pickup_position = [0, 0]
pickup_currently_exists = False
is_game_over = False
direction = "RIGHT"

pygame.init()  # Initialise pygame, I can only set pygame values after this

pygame.display.set_caption("Snake, minmax-pruning")
window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # do I need the extra parenthesis here?

fps = pygame.time.Clock()

############################## at somepoint make a menu ################################

initialise_game()

while not is_game_over:
    # Update
    # move_randomly(snake_position)
    if pickup_currently_exists:
        move_minmax(snake_position, pickup_position)

    snake_body.insert(0, list(snake_position)) # without this, the snake will not move visually
    if snake_position[0] == pickup_position[0] and snake_position[1] == pickup_position[1]:
        score += 1
        pickup_currently_exists = False
    else:
        snake_body.pop() # this is directly related to the snake_body.insert() line. Required.

    if not pickup_currently_exists:
        pickup_position = generate_pickup()
        pickup_currently_exists = True

    # Draw
    # Clear the screen buffer
    window.fill(WHITE)
    # draw the snake
    for pos in snake_body:
        pygame.draw.rect(window, BLACK, pygame.Rect(pos[0], pos[1], snake_body_segment_size, snake_body_segment_size))

    # draw the pickup
    pygame.draw.rect(window, RED, pygame.Rect(
        # a piece of the snake is = to the size of a pickup (10, 10)
        pickup_position[0], pickup_position[1], snake_body_segment_size, snake_body_segment_size))

    # handle x game over conditions
    if snake_position[0] < 0 or snake_position[0] > WINDOW_X - snake_body_segment_size:
        game_over()
    # handle y game over conditions
    if snake_position[1] < 0 or snake_position[1] > WINDOW_Y - snake_body_segment_size:
        game_over()

    for segment in snake_body[1:]:
        if snake_position[0] == segment[0] and snake_position[1] == segment[1]:
            game_over()

    show_score(BLACK, "URW Bookman", 24)

    # Refresh the game display (clear previous frame and draw latest one with parameters specified above)
    pygame.display.update()

    # Set the refresh rate
    fps.tick(snake_speed)
