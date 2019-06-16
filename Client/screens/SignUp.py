from Client.mechanics.Screen import Screen
from Client.mechanics.TextBox import TextBox
from Client.mechanics.Label import Label
from Client.mechanics.NinePatch import NinePatch
from Client.mechanics.TextButton import TextButton
from Client.mechanics.ImageButton import ImageButton
from Client.mechanics.MapObject import MapObject


class SignUp(Screen):
    def __init__(self, world):
        Screen.__init__(self, world, 102, 'images/elements/collage_background.png')
        self.card = NinePatch(self.world, [None, None], 'images/elements/white_cell.9.png', [345, 570], middle=self.bg_image, layer=1)
        self.title = Label(self.world, [None, 70], 'Sign up', 'Large', (41, 182, 246), middle=self.card)
        self.back = ImageButton(self.world, [1008, 20], 'images/elements/light_blue_color.9.png', [35, 35], image='images/elements/white_arrow_right.png', square=28)

        self.username_label = Label(self.world, [410, 160], 'Username', 'Regular', (41, 182, 246))
        self.username_status = MapObject(self.world, [500, 175], image='images/elements/green_v.png', square=16, is_visible=False)
        self.username_text_box = TextBox(self.world, [None, 193], 250, color=(41, 182, 246), middle=self.card)

        self.password_label = Label(self.world, [410, 245], 'Password', 'Regular', (41, 182, 246))
        self.password_status = MapObject(self.world, [500, 175], image='images/elements/green_v.png', square=16, is_visible=False)
        self.password_text_box = TextBox(self.world, [None, 278], 250, color=(41, 182, 246), middle=self.card)

        self.pick = Label(self.world, [410, 330], 'Pick your color', 'Regular', (41, 182, 246))
        self.colors = [ImageButton(self.world, [410 + 50*i, 370], 'images/elements/color_' + str(i+1) + '.9.png', [45, 45]) for i in xrange(5)]
        self.sign_up_button = TextButton(self.world, [None, 450], 'images/elements/dark_blue_box.9.png', [250, 45], text='Sign up', font='Medium', color=(255, 255, 255), middle=self.card)
        self.problem = Label(self.world, [None, 500], '', 'Small', (219, 76, 76), middle=self.card, is_visible=False)
        self.chosen_color = None

    def execute(self):
        pass

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_event(self, event, self.colors + [self.back, self.username_text_box, self.password_text_box, self.sign_up_button] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Screen.draw_screen(self, self.colors + [self.card, self.title, self.back, self.username_label, self.username_status, self.username_text_box, self.password_label, self.password_status, self.password_text_box, self.pick, self.sign_up_button, self.problem] + objects)

    def on_click(self, map_object, event):
        if map_object is self.back:
            from SignIn import SignIn
            self.world.cur_screen = SignIn(self.world)
        elif map_object in self.colors:
            for i in xrange(len(self.colors)):
                if map_object is self.colors[i]:
                    self.chosen_color = i
                    self.colors[i].change_front('images/elements/white_v.png', square=38)
                else:
                    self.colors[i].change_front(None)
        elif map_object is self.sign_up_button:
            self.problem.change_visible(False)
            self.username_text_box.change_background('images/elements/light_blue_cell.9.png')
            self.password_text_box.change_background('images/elements/light_blue_cell.9.png')
            data = self.username_text_box.text
            if len(data) < 6 or len(data) > 15:
                self.username_status = MapObject(self.world, [500, 172], image='images/elements/light_red_x.png', square=16)
                self.username_text_box.change_background('images/elements/light_red_cell.9.png')
                self.problem = Label(self.world, [None, 495], 'Username must contain 6 - 15 characters', 'Small', (219, 76, 76), middle=self.card)
            elif self.world.client.check_username(data):
                self.username_status = MapObject(self.world, [500, 172], image='images/elements/light_red_x.png', square=16)
                self.username_text_box.change_background('images/elements/light_red_cell.9.png')
                self.problem = Label(self.world, [None, 495], 'Username already exists', 'Small', (219, 76, 76), middle=self.card)
            else:
                self.username_status = MapObject(self.world, [500, 175], image='images/elements/green_v.png', square=16)

                data = self.password_text_box.text
                if len(data) < 6 or len(data) > 20:
                    self.password_status = MapObject(self.world, [500, 257], image='images/elements/light_red_x.png',
                                                     square=16)
                    self.password_text_box.change_background('images/elements/light_red_cell.9.png')
                    self.problem = Label(self.world, [None, 495], 'Password must contain 6 - 20 characters', 'Small',
                                         (219, 76, 76), middle=self.card)
                else:
                    self.password_status = MapObject(self.world, [500, 260], image='images/elements/green_v.png',
                                                     square=16)
                    if not self.chosen_color:
                        self.problem = Label(self.world, [None, 495], 'You must pick a color',
                                             'Small',
                                             (219, 76, 76), middle=self.card)
                    else:
                        from SignIn import SignIn
                        self.world.client.create_player(self.username_text_box.text, self.password_text_box.text, 101 + self.chosen_color)
                        self.world.cur_screen = SignIn(self.world)

    def on_type(self, map_object, event):
        if map_object in [self.username_text_box, self.password_text_box]:
            map_object.on_type(event)

    def layer_reorder(self):
        pass
