class StarNode:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0

    def equals(self, other):
        return self.pos == other.pos
