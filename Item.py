from World import World


class Item:
    def __init__(self, image, name, id, is_male, is_used, min_level):
        self.image = image
        self.name = name
        self.id = id
        self.is_used = is_used
        self.min_level = min_level
