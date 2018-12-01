from Screen import Screen
from TextBox import TextBox
from Label import Label


class Login(Screen):
    def __init__(self, world):
        Screen.__init__(self, world, 101, 'images/test_map.png')
        self.buttons = [TextBox(self.world, (380, 200), 300),
                        TextBox(self.world, (380, 270), 300),
                        Label(self.world, (300, 215), 'Username:', 'Title'),
                        Label(self.world, (300, 285), 'Password:', 'Title')]

    def execute(self):
        pass

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_event(self, event, self.buttons + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Screen.draw_screen(self, self.buttons + objects)

    def on_click(self, map_object, event):
        print map_object

    def on_type(self, map_object, event):
        map_object.on_type(event)
