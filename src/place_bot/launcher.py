from solutions.my_robot_eval import MyRobotEval
from spg_overlay.utils.screen_recorder import ScreenRecorder
from spg_overlay.utils.team_info import TeamInfo
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
        self.nb_rounds = 1

        self.team_info = TeamInfo()

        # Create a map only to retrieve const data associated with the map
        # Should be improved...
        my_map = MyMap()
        self.number_robots = my_map.number_robots
        self.time_step_limit = my_map.time_step_limit
        self.real_time_limit = my_map.real_time_limit
        self.number_wounded_persons = my_map.number_wounded_persons
        self.size_area = my_map.size_area

        self.real_time_limit_reached = False
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

        my_map.explored_map.reset()

        my_gui.run()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.go()
