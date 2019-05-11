from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch


class TradeMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [100, -10], 'images/test_text_box.9.png', [800, 340], layer=8)
        self.player = None
        # All cells
        self.all_cells = []
        for i in xrange(5):
            for j in xrange(4):
                if len(self.world.cur_player.items) > 4 * i + j:
                    self.all_cells.append([self.world.cur_player.items[4 * i + j].item_id,
                                           ImageButton(self.world, [630 + j * 63, 5 + i * 63], 'images/cell.9.png', [58, 58],
                                                       front='images/' + self.world.cur_player.items[4 * i + j].item_id +
                                                        '.png',
                                                  square=50)])
                else:
                    self.all_cells.append([-1, ImageButton(self.world, [630 + j * 63, 5 + i * 63], 'images/cell.9.png',
                                                       [58, 58], square=50)])

        # Self cells
        self.self_cells = []
        for i in xrange(3):
            for j in xrange(3):
                self.self_cells.append([-1, ImageButton(self.world, [420 + j * 63, 130 + i * 63], 'images/cell.9.png',
                                                        [58, 58], square=50)])

        # Player cells
        self.player_cells = []
        for i in xrange(3):
            for j in xrange(3):
                self.player_cells.append([-1, ImageButton(self.world, [120 + j * 63, 130 + i * 63], 'images/cell.9.png',
                                                          [58, 58], square=50)])

        self.change_visible(False)
        self.change_clickable(False)

    def place_item(self, index):
        for i in self.self_cells:
            if i[0] == -1:
                i[0] = self.all_cells[index][0]
                i[1].change_image('images/' + str(i[0]) + '.png', square=50)
                break
        self.all_cells[index][0] = -1
        self.all_cells[index][1].front = None

    def remove_item(self, index):
        for i in self.all_cells:
            if i[0] == -1:
                i[0] = self.self_cells[index][0]
                i[1].change_image('images/' + str(i[0]) + '.png', square=50)
                break
        self.self_cells[index][0] = -1
        self.self_cells[index][1].front = None

    def player_place_item(self, item):
        for i in self.player_cells:
            if i[0] == -1:
                i[0] = item
                i[1].change_image('images/' + str(i[0]) + '.png', square=50)
                break

    def player_remove_item(self, index):
        self.player_cells[index][0] = -1
        self.player_cells[index][1].front = None

    def change_visible(self, is_visible=None):
        if is_visible:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        for i in self.all_cells + self.self_cells + self.player_cells:
            i[1].change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        for i in self.all_cells + self.self_cells + self.player_cells:
            i[1].change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.world.draw(self.world.cur_player.surface, [480, 35])
            self.world.draw(self.world.cur_player.text_object.surface, [475, 105])
            if self.world.cur_player.balloon:
                self.world.draw(self.world.cur_player.balloon.surface, [425, 35])

            if self.player:
                self.world.draw(self.player.surface, [185, 35])
                self.world.draw(self.player.text_object.surface, [180, 105])
                if self.player.balloon:
                    self.world.draw(self.player.balloon.surface, [130, 35])

            for i in self.all_cells + self.self_cells + self.player_cells:
                i[1].draw_object()
