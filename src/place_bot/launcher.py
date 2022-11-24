from place_bot.solutions.my_robot_eval import MyRobotEval
from place_bot.spg_overlay.utils.screen_recorder import ScreenRecorder
from place_bot.spg_overlay.gui_map.gui_sr import GuiSR

from place_bot.maps.map_intermediate_01 import MyMapIntermediate01
from place_bot.maps.map_complete_01 import MyMapComplete01
from place_bot.maps.map_complete_02 import MyMapComplete02


# from place_bot.solutions.my_robot_random import MyRobotRandom


class MyMap(MyMapComplete02):
    pass


class MyRobot(MyRobotEval):
    pass


if __name__ == "__main__":
    my_map = MyMap(robot_type=MyRobot)
    my_gui = GuiSR(the_map=my_map)
    my_gui.run()
