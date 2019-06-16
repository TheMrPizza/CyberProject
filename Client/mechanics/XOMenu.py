from NinePatch import NinePatch
from MapObject import MapObject
from ImageButton import ImageButton


class XOMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [800, 340], middle=world.cur_screen.bg_image, layer=8)
        self.grid = MapObject(world, [410, 20], image='images/elements/grid.png', size=[280, 280], layer=9)
        self.stage = MapObject(world, [163, -10], image='images/stage.png', layer=9)
        self.player = None
        self.letter = ''
        self.cells = []
        for i in xrange(3):
            self.cells.append([])
            for j in xrange(3):
                self.cells[i].append([' ', ImageButton(world, [415 + 90 * j, 25 + 90 * i], 'images/area.9.png', [90 ,90], square=60)])

        self.change_visible(False)
        self.change_clickable(False)

    def play_turn(self, letter, row, col):
        if letter == 'X':
            self.cells[row][col][0] = 'X'
            self.cells[row][col][1].change_front('images/elements/light_red_x.png', square=60)
        else:
            self.cells[row][col][0] = 'O'
            self.cells[row][col][1].change_front('images/elements/light_blue_o.png', square=60)
        self.cells[row][col][1].change_clickable(False)

        if letter == self.letter:
            self.stage.pos = [163, -10]
        else:
            self.stage.pos = [738, -10]

        for i in self.cells:
            for j in i:
                if j[0] == ' ':
                    j[1].change_clickable()

    def check_winner(self):
        for i in self.cells:
            if i[0][0] == i[1][0] == i[2][0] != ' ':
                return i[0][0]
        for i in xrange(len(self.cells[0])):
            if self.cells[0][i][0] == self.cells[1][i][0] == self.cells[2][i][0] != ' ':
                return self.cells[0][i][0]
        if self.cells[0][0][0] == self.cells[1][1][0] == self.cells[2][2][0] != ' ':
            return self.cells[0][0][0]
        if self.cells[0][2][0] == self.cells[1][1][0] == self.cells[2][0][0] != ' ':
            return self.cells[0][2][0]

        count = 0
        for i in self.cells:
            for j in i:
                if j[0] != ' ':
                    count += 1
        if count == 9:
            return 'XO'
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

    def change_cells_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        for i in self.cells:
            for j in i:
                j[1].change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.stage.draw_object()

            pos = self.world.cur_player.pos
            self.world.cur_player.update_pos([785, 145])
            if self.world.cur_player.balloon:
                self.world.cur_player.balloon.update([705, 205])
            self.world.cur_player.draw_object()
            self.world.cur_player.update_pos(pos)

            pos = self.player.pos
            self.player.update_pos([210, 145])
            if self.player.balloon:
                self.player.balloon.update([260, 205])
            self.player.draw_object()
            self.player.update_pos(pos)

            for i in self.cells:
                for j in i:
                    j[1].draw_object()
            self.grid.draw_object()
