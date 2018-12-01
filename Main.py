from World import World
from Login import Login
from Beach import Beach
from Player import Player


def main():
    world = World()
    # world.cur_screen = Login(world)
    b = Beach(world)
    b.players = [Player(world, 'guy1guy1', True, [], 15, '23.11.18', True, 201, [200, 300])]
    world.cur_screen = b


if __name__ == '__main__':
    main()
