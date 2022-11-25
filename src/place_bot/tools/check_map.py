from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.gui_sr import GuiSR

from maps.map_intermediate_01 import MyMapIntermediate01
from maps.map_complete_01 import MyMapComplete01
from maps.map_complete_02 import MyMapComplete02


class MyMap(MyMapComplete02):
    pass


class MyRobot(RobotAbstract):

    def control(self):
        pass


if __name__ == "__main__":
    print("")
    my_robot = MyRobot
    my_map = MyMap(robot=my_robot)

    my_gui = GuiSR(the_map=my_map,
                   use_mouse_measure=True)

    my_gui.run()
