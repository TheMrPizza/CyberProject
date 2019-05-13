from NinePatch import NinePatch
from MapObject import MapObject
from ImageButton import ImageButton


class XOMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [100, -10], 'images/test_text_box.9.png', [800, 340], layer=8)

        self.grid = MapObject(world, [400, 30], image='images/grid.png', size=[280, 280], layer=9)
        self.stage = MapObject(world, [130, -10], image='images/stage.png')
        self.player = None
        self.letter = ''
        self.cells = []
        for i in xrange(3):
            self.cells.append([])
            for j in xrange(3):
                self.cells[i].append([' ', ImageButton(world, [405 + 90 * j, 40 + 90 * i], 'images/area.9.png', [90 ,90], square=60)])

        self.change_visible(False)
        self.change_clickable(False)

    def play_turn(self, letter, row, col):
        if letter == 'X':
            self.cells[row][col][0] = 'X'
            self.cells[row][col][1].change_front('images/x_sign.png')
        else:
            self.cells[row][col][0] = 'O'
            self.cells[row][col][1].change_front('images/o_sign.png')

        if letter == self.letter:
            self.stage.pos = [130, -10]
        else:
            self.stage.pos = [650, -10]

        for i in self.cells:
            for j in i:
                if j[0] != ' ':
                    j[1].change_clickable()

    def check_winner(self):
        for i in self.cells:
            if i[0][0] == i[1][0] == i[2][0]:
                return i[0][0]
        for i in xrange(len(self.cells)):
            if self.cells[i][0][0] == self.cells[i][1][0] == self.cells[i][2][0]:
                return self.cells[i][0][0]
        if self.cells[0][0][0] == self.cells[1][1][0] == self.cells[2][2][0]:
            return self.cells[0][0][0]
        if self.cells[0][2][0] == self.cells[1][1][0] == self.cells[2][0][0]:
            return self.cells[0][2][0]
        return None

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.grid.change_visible(change)
        self.stage.change_visible(change)
        for i in self.cells:
            for j in i:
                j[1].change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.grid.change_clickable(change)
        self.stage.change_clickable(change)
        for i in self.cells:
            for j in i:
                j[1].change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.stage.draw_object()

            pos = self.world.cur_player.pos
            self.world.cur_player.update_pos([700, 150])
            if self.world.cur_player.balloon:
                self.world.cur_player.balloon.update([620, 210])
            self.world.cur_player.draw_object()
            self.world.cur_player.update_pos(pos)

            pos = self.player.pos
            self.player.update_pos([180, 150])
            if self.player.balloon:
                self.player.balloon.update([230, 210])
            self.player.draw_object()
            self.player.update_pos(pos)

            for i in self.cells:
                for j in i:
                    j[1].draw_object()
            self.grid.draw_object()
