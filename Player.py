from World import World


class Player:
    def __init__(self, username, is_male, items, level, join_date, is_admin, room_id, room_pos):
        self.username = username
        self.is_male = is_male
        self.items = items
        self.level = level
        self.join_date = join_date
        self.is_admin = is_admin
        self.room_id = room_id
        self.room_pos = room_pos
