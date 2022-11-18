from solutions.my_robot_eval import MyRobotEval
from spg_overlay.utils.screen_recorder import ScreenRecorder
from spg_overlay.gui_map.gui_sr import GuiSR

from maps.map_intermediate_01 import MyMapIntermediate01
from maps.map_complete_01 import MyMapComplete01
from maps.map_complete_02 import MyMapComplete02


# from solutions.my_robot_random import MyRobotRandom


class MyMap(MyMapComplete01):
    pass


class MyRobot(MyRobotEval):
    pass


class Launcher:
    def __init__(self):
        self.video_capture_enabled = False

    def go(self):
        my_map = MyMap()
        playground = my_map.construct_playground(robot_type=MyRobot)

        if self.video_capture_enabled:
            filename_video_capture = self.save_data.path + "/screen.avi".format()
        else:
            filename_video_capture = None

        my_gui = GuiSR(playground=playground,
                       the_map=my_map,
                       draw_interactive=False,
                       filename_video_capture=filename_video_capture)

        my_gui.run()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.go()
