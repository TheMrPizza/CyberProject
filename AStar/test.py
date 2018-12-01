import pygame
import sys
import math
import random

arr = []


class Graph:
    def __init__(self, grid):
        self.grid = grid
        self.weights = {}

    def neighbors(self, parent, goal):
        points = []
        for x in [-20, 0, 20]:
            for y in [-20, 0, 20]:
                if not (x == 0 and y == 0) and 0 <= parent.pos[0] + x < 600 and 0 <= parent.pos[1] + y < 600:
                    if not self.grid[(parent.pos[0]+x-2)/20][(parent.pos[1]+y-2)/20].is_wall:
                        points += [StarNode(self.grid[(parent.pos[0]+x-2)/20][(parent.pos[1]+y-2)/20])]
                        points[-1].g = parent.g + self.cost(parent.pos, points[-1].pos)
                        points[-1].h = self.cost(points[-1].pos, goal.pos)
                        points[-1].f = points[-1].g + points[-1].h
        return points

    def cost(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)  # Distance


class StarNode:
    def __init__(self, grid, parent=None):
        self.parent = parent
        self.grid = grid
        self.pos = grid.x, grid.y
        self.f = 0
        self.g = 0
        self.h = 0

    def equals(self, other):
        return self.pos == other.pos


class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surf = pygame.Rect(x, y, 15, 15)
        self.is_wall = random.randint(0, 2) == 0
        self.is_passed = False


def second_search():
    global arr
    print 'Goal: ' + str(arr[len(arr)-1][len(arr[0])-1].x) + ' ' + str(arr[len(arr)-1][len(arr[0])-1].y)
    graph = Graph(arr)
    start_node = StarNode(arr[0][len(arr[0])-1])
    goal_node = StarNode(arr[len(arr)-1][0])

    open_list = [start_node]
    closed_list = []

    start_node.f = graph.cost(start_node.pos, goal_node.pos)

    while open_list:
        import time
        time.sleep(0.05)
        index = 0

        for i in xrange(len(open_list)):
            if open_list[i].f < open_list[index].f:
                index = i
        cur_node = open_list[index]
        arr[(cur_node.grid.x - 2) / 20][(cur_node.grid.y - 2) / 20].is_passed = True

        if cur_node.equals(goal_node):
            print 'Yay!'
            return

        open_list.remove(cur_node)
        closed_list.append(cur_node)

        for i in graph.neighbors(cur_node, goal_node):
            # print (i.pos[0]-2)/20, (i.pos[1]-2)/20
            is_found = False
            for j in closed_list:
                if i.pos == j.pos:
                    is_found = True
                    break

            if is_found:
                continue

            cost = cur_node.g + graph.cost(cur_node.pos, i.pos)

            is_found = False
            for j in open_list:
                if i.pos == j.pos:
                    is_found = True
                    break
            if not is_found:
                open_list.append(i)
            elif cost >= i.g:
                continue

            # print i.pos
            # world.cur_screen.players[0].x = i.pos[0]
            # world.cur_screen.players[0].y = i.pos[1]

            i.g = cost
            i.h = graph.cost(i.pos, goal_node.pos)
            i.f = i.g + i.h
            i.parent = cur_node
    print 'Nope'
    return


def main():
    global arr
    arr = []
    for i in xrange(30):
        arr.append([])
        for j in xrange(30):
            arr[i].append(Grid(i*20+2, j*20+2))
    import threading
    a = threading.Thread(target=second_search)
    a.start()
    pygame.init()
    surf = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Cyber!")
    clock = pygame.time.Clock()
    while True:
        surf.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i in arr:
            for j in i:
                if j.is_wall:
                    pygame.draw.rect(surf, (0, 0, 0), j.surf)
                elif j.is_passed:
                    pygame.draw.rect(surf, (125, 166, 232), j.surf)
                else:
                    pygame.draw.rect(surf, (209, 209, 209), j.surf)

        pygame.display.update()
        clock.tick(5)


main()
