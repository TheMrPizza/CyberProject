from World import World
from Login import Login


def main():
    world = World()
    world.cur_screen = Login(world)


if __name__ == '__main__':
    main()
