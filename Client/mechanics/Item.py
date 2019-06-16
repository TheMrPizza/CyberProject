from MapObject import MapObject


class Item(MapObject):
    def __init__(self, world, data, pos, amount, is_used, **kwargs):
        MapObject.__init__(self, world, pos, image='images/items/' + data['item_id'] + '.png', **kwargs)
        self.item_id = data['item_id']
        self.title = data['title']
        self.min_level = data['min_level']
        self.item_pos = data['item_pos']
        self.type = data['type']
        self.amount = amount
        self.is_used = is_used

    def draw_object(self, is_on_player=True):
        if is_on_player:
            if self.is_used:
                self.world.draw(self.surface, [self.pos[0] + self.item_pos[0],
                                               self.pos[1] + self.item_pos[1]])
        else:
            self.world.draw(self.surface, self.pos)
