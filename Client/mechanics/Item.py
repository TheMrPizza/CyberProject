from MapObject import MapObject


class Item(MapObject):
    def __init__(self, world, data, pos, is_used):
        MapObject.__init__(self, world, pos, image='images/' + data['item_id'] + '.png', is_transparent=not is_used)
        self.item_id = data['item_id']
        self.title = data['title']
        self.gender = data['gender']
        self.min_level = data['min_level']
        self.is_used = is_used
