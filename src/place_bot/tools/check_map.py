from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.gui_sr import GuiSR

from maps.map_intermediate_01 import MyMapIntermediate01
from maps.map_complete_01 import MyMapComplete01
from maps.map_complete_02 import MyMapComplete02


class MyMap(MyMapComplete02):
    pass


class MyRobot(RobotAbstract):
    def define_message_for_all(self):
        pass

    def control(self):
        pass


if __name__ == "__main__":
    for environment_type in MyMap.environment_series:
        print("")
        print("*** Environment '{}'".format(environment_type.name.lower()))
        my_map = MyMap(environment_type)
        playground = my_map.construct_playground(robot_type=MyRobot)

        my_gui = GuiSR(playground=playground,
                       the_map=my_map,
                       use_mouse_measure=True)

        my_gui.run()
