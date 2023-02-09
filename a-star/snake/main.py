import pygame, time, random, sys, heapq


def initialise_game():
    global score
    score = 0

    # Set game values
    # defining snake default position
    global snake_position_sam
    snake_position_sam = [100, 50]

    global snake_position_charlie
    snake_position_charlie = [400, 400]

    # defining first 4 blocks of snake
    # body
    global snake_body_sam
    snake_body_sam = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]

    global snake_body_charlie
    snake_body_charlie = [[400, 400],
                      [390, 400],
                      [380, 400],
                      [370, 400]
                      ]

    # fruit position
    global pickup_position
    pickup_position = generate_pickup()
    global pickup_currently_exists
    pickup_currently_exists = True


def snake_out_of_bounds(snake_pos, snake_bod):
    if snake_pos[0] < 0 or snake_pos[0] > WINDOW_X - snake_body_segment_size:
        game_over()
    # handle y game over conditions
    if snake_pos[1] < 0 or snake_pos[1] > WINDOW_Y - snake_body_segment_size:
        game_over()

    for segment in snake_bod[1:]:
        if snake_pos[0] == segment[0] and snake_pos[1] == segment[1]:
            game_over()


# displaying Score function
def show_score(font, size):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object
    # score_surface
    score_surface_sam = score_font.render('Score : ' + str(score_sam), True, BLUE)
    score_surface_charlie = score_font.render('Score : ' + str(score_charlie), True, BLACK)

    # create a rectangular object for the
    # text surface object
    score_rect_sam = score_surface_sam.get_rect()
    score_rect_charlie = score_surface_sam.get_rect()

    # displaying text
    global window
    window.blit(score_surface_sam, (100, 0))
    window.blit(score_surface_charlie, (1100, 0))


def generate_pickup():
    return [random.randrange(1, (WINDOW_X / 10)) * 10,
            random.randrange(1, (WINDOW_Y / 10)) * 10]


def move_snake(current_snake_position, move_dir):
        if move_dir == 0:  # up
            current_snake_position[1] -= 10
            return "UP"
        if move_dir == 1:  # down
            current_snake_position[1] += 10
            return "DOWN"
        if move_dir == 2:  # left
            current_snake_position[0] -= 10
            return   "LEFT"
        if move_dir == 3:  # right
            current_snake_position[0] += 10


def get_neighbours(node, direction):
    list_of_nodes = []

    # get adjacent nodes up, down, left, and right of the current nodes
    # returning single number
    down_node = (node[0], node[1] + 10)  # down
    up_node = (node[0], node[1] - 10)  # up
    left_node = (node[0] + 10, node[1])  # left
    right_node = (node[0] - 10, node[1])  # right

    # only return nodes which are not directly opposite to the current direction
    if direction == "UP":
        list_of_nodes.insert(1, up_node)
        list_of_nodes.insert(2, left_node)
        list_of_nodes.insert(3, right_node)
    elif direction == "DOWN":
        list_of_nodes.insert(1, down_node)
        list_of_nodes.insert(2, left_node)
        list_of_nodes.insert(3, right_node)
    elif direction == "LEFT":
        list_of_nodes.insert(1, left_node)
        list_of_nodes.insert(2, up_node)
        list_of_nodes.insert(3, down_node)
    elif direction == "RIGHT":
        list_of_nodes.insert(1, right_node)
        list_of_nodes.insert(2, up_node)
        list_of_nodes.insert(3, down_node)

    return list_of_nodes


def get_current_direction(prev_node, curr_node):
    if prev_node[0] > curr_node[0]:
        return "DOWN"
    elif prev_node[0] < curr_node[0]:
        return "UP"
    elif prev_node[1] > prev_node[1]:
        return "RIGHT"
    elif prev_node[1] < prev_node[1]:
        return "LEFT"


# Use A* pathfinding to move towards the pickup
# A* is a small extension to Dijkstra that uses a heuristic that says: "we're getting a bit closer"
# https://www.youtube.com/watch?v=ySN5Wnu88nE
def a_star_pathfinding(current_snake_position, current_pickup_position):
    global direction_sam
    # Get the start and end of the grid to generate
    start = (current_snake_position[0], current_snake_position[1])
    end = (current_pickup_position[0], current_pickup_position[1])

    # Create two lists: Open (created but not visited) and Closed (contains visited nodes)
    # g(n) cost from the start node to the current node
    # h(n) cost from the current node to the target node
    # f(n) cost from the start node to the target node

    # Create the 'game board' so that I can work out the positions of nodes for a distance check
    # in this instance each node is always 10 away from one another giving me a consistent metric.
    # for A* to work really well you need to have this consistency so that the distance measured is accurate
    all_nodes = []
    for x in range(0, WINDOW_X, snake_body_segment_size):
        for y in range(0, WINDOW_Y, snake_body_segment_size):
            all_nodes.append([x, y])

    open_queue = [start]
    closed_queue = []
    final_node = ()
    current_direction = direction_sam
    previous_node = start
    while len(open_queue) > 0:
        current_node = open_queue.pop()
        closed_queue.insert(1, current_node)
        # if the goal has been reached, exit the loop!
        if current_node[0] == end[0] and current_node[1] == end[1]:
            while len(closed_queue) > 1:
                final_node = closed_queue.pop()
        # neighbour here actually means the 'x' and 'y' values (position) of the node
        # so get three values (depending on current dir), and if they're not in the closed_queue, sort and store them
        # work out direction and assign it to new_direction
        if not current_node == start: # don't run this unless the current node is != to start
            current_direction = get_current_direction(previous_node, current_node)
        node_list = get_neighbours(current_node, current_direction)
        sorted_node_dict = {}
        for node in node_list:
            if node not in closed_queue:
                # arrange them by distance to pickup (my only heuristic) and add to open_queue
                print(node)
                node_distance_node = distance_between_pickup(node, current_pickup_position)
                node_distance = node_distance_node[0] + node_distance_node[1]
                print(node_distance)
                sorted_node_dict[node_distance] = node
        # I'm not sure if this will be added into open_queue in the right order
        sorted_node_dict = dict(sorted(sorted_node_dict.items()))
        for value in sorted_node_dict.values():
            open_queue.insert(1, value)
        previous_node = current_node

    # move the snake to the node closest to the
    current_snake_position = final_node


def distance_between_pickup(s_pos, p_pos):
    x_dist = abs(s_pos[0] - p_pos[0])
    y_dist = abs(s_pos[1] - p_pos[1])

    return [x_dist, y_dist]


def move_closest_to_pickup(current_snake_position, current_pickup_position, direction):
    has_moved = False
    distance = distance_between_pickup(current_snake_position, current_pickup_position)
    while not has_moved:
        print(direction)
        print(distance)
        if distance[1] > 0 and not direction == "DOWN":
            direction = move_snake(current_snake_position, 0)
            has_moved = True
        elif distance[1] < 0 and not direction == "UP":
            direction = move_snake(current_snake_position, 1)
            has_moved = True
        if distance[0] > 0 and not direction == "RIGHT":
            direction = move_snake(current_snake_position, 2)
            has_moved = True
        elif distance[0] < 0 and not direction == "LEFT":
            direction = move_snake(current_snake_position, 3)
            has_moved = True
    print(direction)
    return direction


def move_randomly(current_snake_position, direction):
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
        direction = move_snake(current_snake_position, move_dir)
        has_moved = True
    return direction


# game over function
def game_over():
    # creating font object my_font
    my_font = pygame.font.SysFont('urw bookman', 42)

    # creating a text surface on which text
    # will be drawn
    global score_sam
    global score_charlie
    game_over_surface_sam = my_font.render('Sams Score is : ' + str(score_sam), True, BLACK)
    game_over_surface_charlie = my_font.render('Charlies Score is : ' + str(score_charlie), True, BLACK)

    # blit will draw the text on screen
    global window
    window.blit(game_over_surface_sam, (WINDOW_X / 2, WINDOW_Y / 2))
    window.blit(game_over_surface_charlie, (WINDOW_X / 2, WINDOW_Y / 4))
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
# set the colours for the game.
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)

# Create global values
score_sam = 0
score_charlie = 0
snake_position_sam = [0, 0]
snake_body_sam = [[0, 0]]
snake_position_charlie = [0, 0]
snake_body_charlie = [[0, 0]]
snake_body_segment_size = 10
snake_speed = 60
direction_sam = "RIGHT"
direction_charlie = "RIGHT"
# This is a much better way of representing directions.
dirs = [[10, 0], [0, 10], [-10, 0], [0, -10]]
pickup_position = [0, 0]
pickup_currently_exists = False
is_game_over = False

pygame.init()  # Initialise pygame, I can only set pygame values after this

pygame.display.set_caption("Snake, path-finding")
window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # do I need the extra parenthesis here?

fps = pygame.time.Clock()

############################## at somepoint make a menu ################################

initialise_game()

while not is_game_over:
    # Update
    for event in pygame.event.get(): # check if the player is trying to quit the game and if so close the window safely
        if event.type == pygame.QUIT:
            pygame.quit()  # quits the pygame module NOT the application
            # quits the application (https://stackoverflow.com/questions/1997710/pygame-error-display-surface-quit-why)
            sys.exit()

    # Move Charlie THEN move sam
    direction_charlie = move_randomly(snake_position_charlie, direction_charlie)
    snake_body_charlie.insert(0, list(snake_position_charlie))  # without this, the snake will not move visually
    if snake_position_charlie[0] == pickup_position[0] and snake_position_charlie[1] == pickup_position[1]:
        score_charlie += 1
        pickup_currently_exists = False
    else:
        snake_body_charlie.pop()  # this is directly related to the snake_body.insert() line. Required.

    if pickup_currently_exists:
        a_star_pathfinding(snake_position_sam, pickup_position)
        #move_closest_to_pickup(snake_position_sam, pickup_position, direction_sam)
    snake_body_sam.insert(0, list(snake_position_sam))  # without this, the snake will not move visually
    if snake_position_sam[0] == pickup_position[0] and snake_position_sam[1] == pickup_position[1]:
        score_sam += 1
        pickup_currently_exists = False
    else:
        snake_body_sam.pop()  # this is directly related to the snake_body.insert() line. Required.

    if not pickup_currently_exists:
        pickup_position = generate_pickup()
        pickup_currently_exists = True

    # Draw
    # Clear the screen buffer
    window.fill(WHITE)
    # draw the snake/s
    for pos in snake_body_sam:
        pygame.draw.rect(window, BLACK, pygame.Rect(pos[0], pos[1], snake_body_segment_size, snake_body_segment_size))

    for pos in snake_body_charlie:
        pygame.draw.rect(window, BLUE, pygame.Rect(pos[0], pos[1], snake_body_segment_size, snake_body_segment_size))

    # draw the pickup
    pygame.draw.rect(window, RED, pygame.Rect(
        # a piece of the snake is = to the size of a pickup (10, 10)
        pickup_position[0], pickup_position[1], snake_body_segment_size, snake_body_segment_size))

    # handle game over conditions for snakes
    snake_out_of_bounds(snake_position_sam, snake_body_sam)
    snake_out_of_bounds(snake_position_charlie, snake_body_charlie)

    show_score("URW Bookman", 24)

    # Refresh the game display (clear previous frame and draw latest one with parameters specified above)
    pygame.display.update()

    # Set the refresh rate
    fps.tick(snake_speed)
