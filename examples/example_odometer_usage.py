"""
This example demonstrates the correct usage of the odometer sensor.

The odometer returns an INTEGRATED position estimate (x, y, orientation),
NOT the raw displacement values (dist_travel, alpha, theta).

This example shows:
1. How to read the odometer values
2. How to access raw displacement (for debugging)
3. How the odometer position differs from true position due to noise accumulation
"""

import os
import sys
import math

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from place_bot.simulation.gui_map.closed_playground import ClosedPlayground
from place_bot.simulation.gui_map.simulator import Simulator
from place_bot.simulation.gui_map.world_abstract import WorldAbstract
from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_abstract import RobotAbstract


class MyRobotOdometer(RobotAbstract):
    """
    A robot that moves in a square pattern and displays odometer information.
    """
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.state = 0  # 0: forward, 1: turn
        
    def control(self) -> CommandsDict:
        """
        Move in a square pattern.
        """
        # Print odometer information every 30 steps
        if self.counter % 30 == 0:
            self.print_odometer_info()
        
        self.counter += 1
        
        # State machine for square movement
        if self.state == 0:  # Moving forward
            if self.counter % 100 == 0:
                self.state = 1  # Start turning
                self.turn_counter = 0
            return {"forward": 1.0, "rotation": 0.0}
        else:  # Turning
            self.turn_counter = getattr(self, 'turn_counter', 0) + 1
            if self.turn_counter > 25:  # Turn for 25 steps (roughly 90 degrees)
                self.state = 0  # Go forward again
            return {"forward": 0.0, "rotation": 1.0}
    
    def print_odometer_info(self):
        """
        Print odometer information to demonstrate its usage.
        """
        print("\n" + "="*60)
        print(f"Step {self.counter}")
        
        # Get the integrated position estimate from odometer
        if not self.odometer_is_disabled():
            odom_pose = self.odometer_values()
            if odom_pose is not None:
                x_est, y_est, orient_est = odom_pose
                print(f"Odometer estimate: x={x_est:7.2f}, y={y_est:7.2f}, θ={orient_est:6.3f} rad")
            
            # Get raw displacement (for debugging)
            dist, alpha, theta = self.odometer_last_displacement()
            print(f"Last displacement: dist={dist:6.2f}, α={alpha:6.3f}, θ={theta:6.3f}")
        
        # Compare with true position (only for debugging, not for control!)
        true_pos = self.true_position()
        true_angle = self.true_angle()
        print(f"True position:     x={true_pos[0]:7.2f}, y={true_pos[1]:7.2f}, θ={true_angle:6.3f} rad")
        
        # Calculate error
        if not self.odometer_is_disabled():
            odom_pose = self.odometer_values()
            if odom_pose is not None:
                x_est, y_est, orient_est = odom_pose
                position_error = math.sqrt((x_est - true_pos[0])**2 + (y_est - true_pos[1])**2)
                angle_error = abs(orient_est - true_angle)
                print(f"Position error: {position_error:.2f} pixels")
                print(f"Angle error:    {angle_error:.3f} rad")
        
        print("="*60)


class MyWorldOdometer(WorldAbstract):
    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (800, 800)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        self._robot_pos = ((0, 0), 0)
        self._playground.add(robot, self._robot_pos)


def main():
    print("\n" + "="*60)
    print("ODOMETER USAGE EXAMPLE")
    print("="*60)
    print("\nThe robot will move in a square pattern.")
    print("Odometer information is printed every 30 steps.")
    print("\nKey points:")
    print("- odometer_values() returns INTEGRATED position [x, y, orientation]")
    print("- odometer_last_displacement() returns raw displacement [dist, alpha, theta]")
    print("- The odometer position accumulates errors over time (drift)")
    print("- The red path (if enable_visu_noises=True) shows odometer estimate")
    print("\nPress Q to quit")
    print("="*60 + "\n")
    
    my_robot = MyRobotOdometer()
    my_world = MyWorldOdometer(robot=my_robot)

    # enable_visu_noises : shows the odometer estimated path in red
    simulator = Simulator(the_world=my_world,
                          enable_visu_noises=True,
                          use_keyboard=False)
    simulator.run()


if __name__ == '__main__':
    main()

