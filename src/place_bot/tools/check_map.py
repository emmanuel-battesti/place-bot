from place_bot.spg_overlay.entities.robot_abstract import RobotAbstract
from place_bot.spg_overlay.gui_map.gui_sr import GuiSR

from place_bot.maps.map_intermediate_01 import MyMapIntermediate01
from place_bot.maps.map_complete_01 import MyMapComplete01
from place_bot.maps.map_complete_02 import MyMapComplete02


class MyMap(MyMapComplete02):
    pass


class MyRobot(RobotAbstract):

    def control(self):
        pass


if __name__ == "__main__":
    print("")
    my_map = MyMap(robot_type=MyRobot)

    my_gui = GuiSR(the_map=my_map,
                   use_mouse_measure=True)

    my_gui.run()
