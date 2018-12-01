from MapObject import MapObject
import pygame


class TextBox(MapObject):
    def __init__(self, world, pos, width, middle=None):
        self.box_left = self.load_image(world, 'images/TEXT_BOX_LEFT.png', size=[None, 54])
        self.box = self.load_image(world, 'images/TEXT_BOX_CONTENT.png', size=[width, 54])
        self.box_right = self.load_image(world, 'images/TEXT_BOX_RIGHT.png', size=[None, 54])
        MapObject.__init__(self, world, pos, MapObject.merge_surfaces_horizontal([self.box_left, self.box, self.box_right]), middle=middle, layer=4)
        self.text = ''
        self.text_surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_click(self):
        print 'Someone clicked me!'

    def on_type(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN and self.text != '':
            self.on_send()
            self.text = ''
        elif self.world.fonts['Text Box'].size(self.text + event.unicode)[0] <= self.box.get_size()[0]:
            self.text += event.unicode
        self.text_surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_send(self):
        print self.text  # TODO: Send message to server

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        self.world.draw(self.text_surface, (self.pos[0] + self.box_left.get_size()[0],
                                            MapObject.find_middle(self.text_surface, self)[1]))
