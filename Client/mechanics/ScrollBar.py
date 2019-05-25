from MapObject import MapObject


class ScrollBar(MapObject):
    def __init__(self, world, pos, margin, is_vertical):
        MapObject.__init__(self, world, pos, image='images/test_text_box.9.png', size=[40, 40], is_visible=False, is_clickable=False)
        self.margin = margin
        self.is_vertical = is_vertical
        self.items = []

    def __iter__(self):
        return iter(self.items)

    def append(self, item):
        if len(self.items) > 0:
            if self.is_vertical:
                item.update_pos([item.pos[0], self.pos[1] + len(self.items) * (self.margin + self.items[0].height)])
            else:
                item.update_pos([self.pos[0] + len(self.items) * (self.margin + self.items[0].width), item.pos[1]])
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

    def draw_object(self):
        for i in self.items:
            i.draw_object()
