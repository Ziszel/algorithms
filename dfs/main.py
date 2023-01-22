# an iterative implementation of DFS created with the aid of
# https://www.youtube.com/watch?v=PMMc4VsIacU

def dfs_pre(g, v):
    if v in range(0, len(g)):
        stack = [v]
        while len(stack) > 0:
            v = stack.pop()
            if not marked[v]:
                print(v)
                marked[v] = True
                for neighbour in g[v]:
                    stack.append(neighbour)
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

dfs_pre(G, 0)
print(marked)
