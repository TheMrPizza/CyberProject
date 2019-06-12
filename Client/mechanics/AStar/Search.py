from Graph import Graph
from StarNode import StarNode


def search_path(world, start, goal):
    """
    Finding the shortest path without colliding with obstacles. The function uses A* algorithm, in a grid of 10x10 px.

    :param world: The game's world
    :param start: Start point
    :param goal: End point
    :return: List of tuples of 2 integers - The points in the path if found, otherwise None.
    """

    # Rounding start and goal by 10
    start = start[0]/20*20, start[1]/20*20
    goal = goal[0]/20*20, goal[1]/20*20

    # Initializing the graph and the nodes
    graph = Graph(world)
    start_node = StarNode(pos=start)
    goal_node = StarNode(pos=goal)

    open_list = [start_node]
    closed_list = []

    start_node.f = Graph.cost(start_node.pos, goal_node.pos)

    while open_list:
        index = 0

        for i in xrange(len(open_list)):
            if open_list[i].f < open_list[index].f:
                index = i
        cur_node = open_list[index]

        cur_node.is_passed = True

        if cur_node.equals(goal_node):  # Goal has reached! Creating the path that was found
            path = []
            while cur_node.parent:
                for i in xrange(4):  # Adding mid-points to control walking speed
                    x = cur_node.pos[0] + (cur_node.parent.pos[0] - cur_node.pos[0]) / 4 * i
                    y = cur_node.pos[1] + (cur_node.parent.pos[1] - cur_node.pos[1]) / 4 * i
                    path.append((x, y))
                cur_node = cur_node.parent
            return path

        open_list.remove(cur_node)
        closed_list.append(cur_node)

        # Checking all the possible neighbors
        for i in graph.neighbors(cur_node, goal_node):
            is_found = False
            for j in closed_list:
                if i.pos == j.pos:
                    is_found = True
                    break

            if is_found:
                continue

            cost = cur_node.g + Graph.cost(cur_node.pos, i.pos)

            is_found = False
            for j in open_list:
                if i.pos == j.pos:
                    is_found = True
                    break
            if not is_found:
                open_list.append(i)
            elif cost >= i.g:
                continue

            i.g = cost
            i.h = Graph.cost(i.pos, goal_node.pos)
            i.f = i.g + i.h
            i.parent = cur_node

    # Oh no! Path not found
    print 'Nope'
    return None
