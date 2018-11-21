from Screen import Screen
from TextBox import TextBox


class Login(Screen):
    def __init__(self):
        Screen.__init__(self, 101, None)
        tb = TextBox(100, 100, 300)
