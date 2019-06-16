from MapObject import MapObject
import pygame


class ScrollBar(MapObject):
    def __init__(self, world, pos, margin, is_vertical, size):
        MapObject.__init__(self, world, pos, image='images/elements/light_blue_cell.9.png', size=[40, 40], is_visible=False, is_clickable=False)
        self.RATE = 25
        self.margin = margin
        self.is_vertical = is_vertical
        self.size = size
        self.items = []

    def __iter__(self):
        return iter(self.items)

    def append(self, item):
        if self.is_vertical:
            item.update_pos([self.pos[0], self.pos[1] + len(self.items) * (self.margin + item.height)])
        else:
            item.update_pos([self.pos[0] + len(self.items) * (self.margin + item.width), self.pos[1]])
        self.items.append(item)

    def remove(self, item):
        is_found = False
        for i in self.items:
            if is_found:
                if self.is_vertical:
                    i.update_pos([i.pos[0], i.pos[1] - (self.items[0].height + self.margin)])
                else:
                    i.update_pos([i.pos[0] - (self.items[0].width + self.margin), i.pos[1]])
            if i is item:
                is_found = True
        self.items.remove(item)

    def scroll(self, is_up):
        if self.is_vertical:
            if is_up:
                if self.items[0].pos[1] + self.RATE < self.pos[1]:
                    change = self.RATE
                else:
                    change = self.pos[1] - self.items[0].pos[1]
            else:
                if self.items[-1].pos[1] + self.items[-1].height - self.RATE > self.pos[1] + self.size[1]:
                    change = -self.RATE
                else:
                    change = self.pos[1] + self.size[1] - (self.items[-1].pos[1] + self.items[-1].height)
            for i in self.items:
                i.update_pos([i.pos[0], i.pos[1] + change])
        else:
            if is_up:
                change = -self.RATE if self.items[-1].pos[0] + self.items[-1].width - self.RATE > self.size[0] else self.size[0] - (self.items[-1].pos[0] + self.items[-1].width)
            else:
                change = self.RATE if self.items[0].pos[0] + self.RATE < 0 else -self.items[0].pos[0]
            for i in self.items:
                i.update_pos([i.pos[0], i.pos[1] + change])

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        for i in self.items:
            i.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        for i in self.items:
            i.change_clickable(change)

    def draw_object(self):
        surf = pygame.Surface([self.pos[0] + self.size[0], self.pos[1] + self.size[1]], pygame.SRCALPHA)
        for i in self.items:
            i.draw_item(surf)
        self.world.draw(surf, self.pos, area=(self.pos, self.size))
