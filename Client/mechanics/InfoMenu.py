from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label


class InfoMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [300, -10], 'images/test_text_box.9.png', [480, 340], layer=8)
        self.stage = MapObject(world, [330, -10], image='images/stage.png')
        self.arrow = MapObject(world, [360, 280], image='images/green_arrow.png')
        self.level = Label(world, [385, 270], str(self.world.cur_player.level), 'Level', (82, 175, 46))
        self.cells = []
        for i in xrange(5):
            for j in xrange(4):
                if len(self.world.cur_player.items) > 4 * i + j:
                    self.cells.append([self.world.cur_player.items[4 * i + j].item_id,
                                      ImageButton(self.world, [520 + j * 63, 5 + i * 63], 'images/cell.9.png', [58, 58],
                                                  front='images/' + self.world.cur_player.items[4 * i + j].item_id +
                                                        '.png',
                                                  square=50)])
                else:
                    self.cells.append([-1, ImageButton(self.world, [520 + j * 63, 5 + i * 63], 'images/cell.9.png',
                                                       [58, 58])])

    def change_focus(self):
        self.is_focus = not self.is_focus

    def draw_object(self):
        if self.is_focus:
            NinePatch.draw_object(self)
            self.stage.draw_object()
            player_pos = [375, 146]
            self.world.draw(self.world.cur_player.surface, player_pos)
            for i in self.world.cur_player.items:
                if i.is_used:
                    self.world.draw(i.surface, [player_pos[0] + i.item_pos[0], player_pos[1] + i.item_pos[1]])
            self.world.draw(self.world.cur_player.text_object.surface, [375, 225])
            self.arrow.draw_object()
            self.level.draw_object()
            for i in self.cells:
                i[1].draw_object()