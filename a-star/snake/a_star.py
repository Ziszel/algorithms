import queue

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set the dimensions of the grid
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Directions - used to find the neighbours of a node
DIRS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


class Node:
    # takes in one parameter, the position.
    def __init__(self, position, parent=None):
        self.position = position
        # https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        # The parent is required in order to backtrack, creating the path
        self.parent = parent
        # https://brilliant.org/wiki/a-star-search/
        # g = the cost so far to reach a Node from the starting position
        # h = the estimated cost from the current Node to the target Node (heuristic)
        # f = the total cost of using a node | f(n) = g(n) + f(n)
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    # The heuristic is a simple manhattan distance check (a.x - b.x) + (a.y - b.y)
    # https://www.sciencedirect.com/topics/mathematics/manhattan-distance
    # https://www.sciencedirect.com/science/article/pii/B9780124095205500205
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(start, end, first_snake, second_snake):
    # Create two lists, one to manage the unvisited nodes, and another to manage the visited nodes (open and closed)
    open_list = queue.PriorityQueue()
    closed_list = []

    # Create two Node objects,
    # In this instance it is always the head of a snake, and the Food objects current position respectively
    current_node = Node(start)
    end_node = Node(end)

    # adds the first node into the queue to ready it for iteration
    open_list.put(current_node)

    while not open_list.empty():
        # pops off the first item of the queue (open_list) and set current_node == to it
        current_node = open_list.get()

        # If the snake has reached the target, ready the path to be returned
        if current_node == end_node:
            path = []
            while current_node is not None:
                # Add each Node's, used to reach the end_node, position to the path to be returned
                path.append(current_node.position)
                # Each node has a parent which allows the program to backtrack the path to the first node
                current_node = current_node.parent
            # https://stackoverflow.com/questions/3453085/what-is-double-colon-in-python-when-subscripting-sequences
            # No start or end argument, step = -1
            return path[::-1]

        # Add the current node to the closed list
        closed_list.append(current_node)

        # in each direction surrounding the current node (Down, Up, Left, Right), check to see if it is valid and if
        # so, add it to the open_queue
        for neighbour in DIRS:
            neighbour_pos = (current_node.position[0] + neighbour[0], current_node.position[1] + neighbour[1])

            # bounds check, if the node is out of bounds, skip this node
            if neighbour_pos[0] < 0 \
                    or neighbour_pos[0] >= GRID_WIDTH \
                    or neighbour_pos[1] < 0 \
                    or neighbour_pos[1] >= GRID_HEIGHT:
                continue

            # If the node has already been visited, skip this node
            if neighbour_pos in [node.position for node in closed_list]:
                continue

            # If the next best node is in either of the snake's bodies, skip this node
            if neighbour_pos in first_snake.body or neighbour_pos in second_snake.body:
                continue

            # Get the total cost of moving to the new node
            g = current_node.g + 1
            h = heuristic(neighbour_pos, end_node.position)
            f = g + h

            # Assign the cost to new node. Storing the values in a Node object
            neighbour_node = Node(neighbour_pos, current_node)
            neighbour_node.g = g
            neighbour_node.h = h
            neighbour_node.f = f

            # If the neighbour node has not been visited, add it to the open_list queue
            # https://stackoverflow.com/questions/10406130/check-if-something-is-not-in-a-list-in-python
            # check will ensure neighbour_pos is not already stored in any node's position parameter in the open_list
            if neighbour_pos not in [node.position for node in open_list.queue]:
                open_list.put(neighbour_node)
            # If the node exists in the open_list
            else:
                for node in open_list.queue:
                    # check to see if the node.position is == to the neighbour_pos and if the f score is greater
                    if node.position == neighbour_pos and node.f > neighbour_node.f:
                        # if the f score IS greater, remove it and replace it with the neighbour node as a better
                        # path has been found
                        open_list.queue.remove(node)
                        open_list.put(neighbour_node)
