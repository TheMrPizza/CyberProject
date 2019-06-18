from Resources import colors, fonts, jon_missions, jenny_missions, charles_missions
from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label
from ScrollBar import ScrollBar
from MissionItem import MissionItem


class AgentMenu(NinePatch):
    def __init__(self, world, agent_name):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [700, 340], layer=8, middle=world.cur_screen.bg_image)
        self.agent_name = agent_name
        self.x_button = ImageButton(self.world, [195, 5], 'images/elements/light_red_color.9.png', [30, 30], image='images/elements/white_x.png', square=18)
        self.missions = ScrollBar(self.world, [320, 5], 5, True, [550, 315])
        if self.agent_name == 'Jenny':
            self.agent = MapObject(self.world, [210, 108], image='images/rooms/203/Jenny.png', layer=9)
        elif self.agent_name == 'Jon':
            self.agent = MapObject(self.world, [210, 108], image='images/rooms/201/Jon.png', layer=9)
        elif self.agent_name == 'Charles':
            self.agent = MapObject(self.world, [210, 108], image='images/rooms/204/Charles.png', layer=9)
        self.update_missions()
        self.name = Label(self.world, [None, 210], agent_name, fonts['NPC'], colors[agent_name.lower()], middle=self.agent)
        self.change_visible(False)
        self.change_clickable(False)

    def update_missions(self):
        self.missions.remove_all()
        missions = None
        if self.agent_name == 'Jon':
            missions = jon_missions
        elif self.agent_name == 'Jenny':
            missions = jenny_missions
        elif self.agent_name == 'Charles':
            missions = charles_missions
        for i in missions:
            for j in i:
                if str(j[0]) in self.world.cur_player.missions:
                    if not self.world.cur_player.missions[str(j[0])]:  # Completed mission
                        self.missions.append(MissionItem(self.world, j[0], j[1], j[2], j[3], j[4], j[5], True))
                        break
                else:  # Closed mission
                    self.missions.append(MissionItem(self.world, j[0], j[1], j[2], j[3], j[4], j[5]))
                    break

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.x_button.change_visible(change)
        self.agent.change_visible(change)
        self.name.change_visible(change)
        self.missions.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.x_button.change_clickable(change)
        self.agent.change_clickable(change)
        self.name.change_clickable(change)
        self.missions.change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.x_button.draw_object()
            self.agent.draw_object()
            self.name.draw_object()
            self.missions.draw_object()
