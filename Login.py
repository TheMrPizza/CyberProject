from Screen import Screen
from TextBox import TextBox
from Label import Label


class Login(Screen):
    def __init__(self, world):
        Screen.__init__(self, world, 101, None)
        self.buttons = [TextBox(self.world, 380, 200, 300),
                        TextBox(self.world, 380, 270, 300),
                        Label(self.world, 300, 215, 'Username:', 'Title'),
                        Label(self.world, 300, 285, 'Password:', 'Title')]
