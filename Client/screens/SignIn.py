from Client.mechanics.Screen import Screen
from Client.mechanics.TextBox import TextBox
from Client.mechanics.Label import Label
from Client.mechanics.NinePatch import NinePatch
from Client.mechanics.TextButton import TextButton
from Client.mechanics.MapObject import MapObject
from Loading import Loading
from SignUp import SignUp


class SignIn(Screen):
    def __init__(self, world):
        Screen.__init__(self, world, 101, 'images/elements/collage_background.png')
        self.card = NinePatch(self.world, [700, None], 'images/elements/white_cell.9.png', [345, 570], middle=self.bg_image, layer=1)
        self.title = Label(self.world, [None, 70], 'Sign in', 'Large', (41, 182, 246), middle=self.card)
        self.username_label = Label(self.world, [750, 160], 'Username', 'Regular', (41, 182, 246))
        self.username_text_box = TextBox(self.world, [None, 193], 250, color=(41, 182, 246), middle=self.card)
        self.password_label = Label(self.world, [750, 245], 'Password', 'Regular', (41, 182, 246))
        self.password_text_box = TextBox(self.world, [None, 278], 250, color=(41, 182, 246), middle=self.card)
        self.sign_in_button = TextButton(self.world, [None, 350], 'images/elements/light_blue_box.9.png', [250, 45], text='Sign in', font='Medium', color=(255, 255, 255), middle=self.card)
        self.problem = Label(self.world, [None, 395], '', 'Small', (219, 76, 76), middle=self.card, is_visible=False)
        self.question = Label(self.world, [750, 422], 'New to Volantis?', 'Regular', (21, 101, 192))
        self.sign_up_button = TextButton(self.world, [None, 455], 'images/elements/dark_blue_box.9.png', [250, 45], text='Sign up', font='Medium', color=(255, 255, 255), middle=self.card)

        self.logo = MapObject(self.world, [40, 40], image='images/elements/logo.png')
        self.logo_title1 = Label(self.world, [40, 179], 'Your adventure', 'Big', (44, 101, 144))
        self.logo_title2 = Label(self.world, [40, 250], 'starts now.', 'Big', (44, 101, 144))

    def execute(self):
        pass

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_event(self, event, [self.username_text_box, self.password_text_box, self.sign_in_button, self.sign_up_button] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Screen.draw_screen(self, [self.card, self.title, self.username_label, self.username_text_box, self.password_label, self.password_text_box, self.sign_in_button, self.problem, self.question, self.sign_up_button, self.logo, self.logo_title1, self.logo_title2] + objects)

    def on_click(self, map_object, event):
        if map_object is self.sign_in_button:
            data = self.username_text_box.text
            if data:
                if self.world.client.connect(data):
                    print 'Player connected'
                    self.world.cur_screen = Loading(self.world, 101, None, data)
                else:
                    self.problem = Label(self.world, [None, 395], 'Incorrect username or password', 'Small',
                                         (219, 76, 76), middle=self.card)
        elif map_object is self.sign_up_button:
            self.world.cur_screen = SignUp(self.world)

    def on_type(self, map_object, event):
        if map_object in [self.username_text_box, self.password_text_box]:
            data = map_object.on_type(event)
            if data:
                if self.world.client.connect(data):
                    print 'Player connected'
                    self.world.cur_screen = Loading(self.world, 101, None, data)
                else:
                    self.problem = Label(self.world, [None, 395], 'Incorrect username or password', 'Small',
                                         (219, 76, 76), middle=self.card)

    def layer_reorder(self):
        pass
