
# an iterative implementation of DFS created with the aid of
# https://www.youtube.com/watch?v=xlVX7dXLS64

def bfs(g, v):
    if v in range(0, len(g)):
        queue = [v]
        while len(queue) > 0:
            v = queue.pop(0)
            print(v)
            if not marked[v]:
                marked[v] = True
                for neighbour in g[v]:
                    if not marked[neighbour]:
                        queue.append(neighbour)
    else:
        print ("starting value is less than 0 or greater than graph size")


# define G as an adjacency list
G = {
    0: [1, 2, 3],
    1: [0, 3],
    2: [0, 3],
    3: [0, 1, 2, 4],
    4: [3]
}

# generate a list to track nodes visited
marked = [False] * len(G)

bfs(G, 0)
