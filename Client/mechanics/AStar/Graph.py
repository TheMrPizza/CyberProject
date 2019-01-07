import math
from StarNode import StarNode


class Graph:
    def __init__(self, world):
        self.path = world.cur_screen.path

    def neighbors(self, parent, goal):
        points = []
        for x in [-10, 0, 10]:
            for y in [-10, 0, 10]:
                if not (x == 0 and y == 0) and 0 <= parent.pos[0] + x < self.path.width and 0 <= parent.pos[1] + y < self.path.height:
                    if not self.path.surface.get_at((parent.pos[0]+x, parent.pos[1]+y)).a == 0:
                        points += [StarNode(pos=(parent.pos[0]+x, parent.pos[1]+y))]
                        points[-1].g = parent.g + self.cost(parent.pos, points[-1].pos)
                        points[-1].h = self.cost(points[-1].pos, goal.pos)
                        points[-1].f = points[-1].g + points[-1].h
        return points

    def cost(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)  # Distance
