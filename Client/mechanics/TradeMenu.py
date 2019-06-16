from ImageButton import ImageButton
from NinePatch import NinePatch


class TradeMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [800, 340], middle=world.cur_screen.bg_image, layer=8)
        self.player = None
        self.is_final = False
        # All cells
        self.all_cells = []
        for i in xrange(5):
            for j in xrange(4):
                if len(self.world.cur_player.get_all_items()) > 4 * i + j:
                    self.all_cells.append([self.world.cur_player.get_all_items()[4 * i + j].item_id,
                                           ImageButton(self.world, [663 + j * 63, 5 + i * 63], 'images/elements/light_blue_color.9.png', [58, 58],
                                                       image='images/items/' + self.world.cur_player.get_all_items()[4 * i + j].item_id +
                                                        '.png',
                                                        square=50)])
                else:
                    self.all_cells.append([-1, ImageButton(self.world, [663 + j * 63, 5 + i * 63], 'images/elements/light_blue_color.9.png',
                                                       [58, 58], square=50)])

        # Self cells
        self.self_cells = []
        for i in xrange(3):
            for j in xrange(3):
                self.self_cells.append([-1, ImageButton(self.world, [453 + j * 63, 130 + i * 63], 'images/elements/light_blue_color.9.png',
                                                        [58, 58], square=50)])

        # Player cells
        self.player_cells = []
        for i in xrange(3):
            for j in xrange(3):
                self.player_cells.append([-1, ImageButton(self.world, [153 + j * 63, 130 + i * 63], 'images/elements/light_blue_color.9.png',
                                                          [58, 58], square=50)])
        self.v_button = ImageButton(self.world, [363, 190], 'images/elements/light_green_color.9.png', [60, 30], image='images/elements/white_v.png', square=18)
        self.x_button = ImageButton(self.world, [363, 224], 'images/elements/light_red_color.9.png', [60, 30], image='images/elements/white_x.png', square=13)
        self.change_visible(False)
        self.change_clickable(False)

    def place_item(self, index):
        for i in self.self_cells:
            if i[0] == -1:
                i[0] = self.all_cells[index][0]
                i[1].change_front('images/items/' + str(i[0]) + '.png', square=50)
                break
        self.all_cells[index][0] = -1
        self.all_cells[index][1].front = None

    def remove_item(self, index):
        for i in self.all_cells:
            if i[0] == -1:
                i[0] = self.self_cells[index][0]
                i[1].change_front('images/items/' + str(i[0]) + '.png', square=50)
                break
        self.self_cells[index][0] = -1
        self.self_cells[index][1].front = None

    def player_place_item(self, item):
        for i in self.player_cells:
            if i[0] == -1:
                i[0] = item
                i[1].change_front('images/items/' + str(i[0]) + '.png', square=50)
                break

    def player_remove_item(self, index):
        self.player_cells[index][0] = -1
        self.player_cells[index][1].front = None

    def accept_trade(self):
        if self.is_final:  # Both players approved. Make the trade!
            self_items = [i[0] for i in self.self_cells if i[0] != -1]
            player_items = [i[0] for i in self.player_cells if i[0] != -1]
            self.world.client.make_trade(self.player.username, self_items, player_items)
        else:
            self.world.client.accept_trade(self.player.username)
            self.is_final = True
            for i in self.self_cells:
                i[1].change_bg('images/elements/light_green_color.9.png', [58, 58])

    def player_accept_trade(self):
        self.is_final = True
        for i in self.player_cells:
            i[1].change_bg('images/elements/light_green_color.9.png', [58, 58])

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.v_button.change_visible(change)
        self.x_button.change_visible(change)
        for i in self.all_cells + self.self_cells + self.player_cells:
            i[1].change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.v_button.change_clickable(change)
        self.x_button.change_clickable(change)
        for i in self.all_cells + self.self_cells + self.player_cells:
            i[1].change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)

            pos = self.world.cur_player.pos
            self.world.cur_player.update_pos([513, 24])
            if self.world.cur_player.balloon:
                self.world.cur_player.balloon.update([433, 80])
            self.world.cur_player.draw_object()
            self.world.cur_player.update_pos(pos)

            pos = self.player.pos
            self.player.update_pos([218, 24])
            if self.player.balloon:
                self.player.balloon.update([268, 80])
            self.player.draw_object()
            self.player.update_pos(pos)

            for i in self.all_cells + self.self_cells + self.player_cells:
                i[1].draw_object()
            self.v_button.draw_object()
            self.x_button.draw_object()
