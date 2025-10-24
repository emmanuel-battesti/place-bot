"""
This example demonstrates how to use velocity estimation from the odometer.

The odometer provides raw displacement values (dist, alpha, theta) which can be
interpreted as velocities in pixels/timestep and radians/timestep:
- dist: linear velocity (pixels/timestep)
- theta: angular velocity (radians/timestep)

This example shows:
1. How to use estimated_linear_speed()
2. How to use estimated_angular_speed()
3. How to use estimated_velocity() for both
4. How these values relate to the raw odometer data
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


class MyRobotVelocity(RobotAbstract):
    """
    A robot that demonstrates velocity estimation from the odometer.
    """
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.phase = 0  # 0: accelerate, 1: constant speed, 2: turn
        
    def control(self) -> CommandsDict:
        """
        Control with different phases to show velocity changes.
        """
        # Print velocity information every 20 steps
        if self.counter % 20 == 0:
            self.print_velocity_info()
        
        self.counter += 1
        
        # Phase transitions
        if self.counter == 50:
            self.phase = 1
            print("\n>>> Phase 1: Constant speed <<<\n")
        elif self.counter == 100:
            self.phase = 2
            print("\n>>> Phase 2: Turning <<<\n")
        elif self.counter == 150:
            self.phase = 0
            print("\n>>> Phase 0: Accelerating <<<\n")
        
        # Control based on phase
        if self.phase == 0:  # Accelerating
            progress = min(1.0, self.counter / 50.0)
            return {"forward": progress, "rotation": 0.0}
        elif self.phase == 1:  # Constant speed
            return {"forward": 1.0, "rotation": 0.0}
        else:  # Turning
            return {"forward": 0.5, "rotation": 1.0}
    
    def print_velocity_info(self):
        """
        Print velocity information from the odometer.
        """
        print("\n" + "="*70)
        print(f"Step {self.counter}")
        
        if not self.odometer_is_disabled():
            # Method 1: Individual methods
            linear_speed = self.estimated_linear_speed()
            angular_speed = self.estimated_angular_speed()
            print(f"\nEstimated velocities:")
            print(f"  Linear speed:  {linear_speed:8.3f} pixels/timestep")
            print(f"  Angular speed: {angular_speed:8.3f} rad/timestep")
            
            # Method 2: Combined method
            linear, angular = self.estimated_velocity()
            print(f"\nUsing estimated_velocity():")
            print(f"  Linear:  {linear:8.3f} pixels/timestep")
            print(f"  Angular: {angular:8.3f} rad/timestep")
            
            # Show the raw odometer displacement
            dist, alpha, theta = self.odometer_last_displacement()
            print(f"\nRaw odometer displacement:")
            print(f"  dist:  {dist:8.3f} pixels  (= linear speed)")
            print(f"  alpha: {alpha:8.3f} rad")
            print(f"  theta: {theta:8.3f} rad     (= angular speed)")
            
            # Compare with true velocity (for validation only)
            true_vel = self.true_velocity()
            true_ang_vel = self.true_angular_velocity()
            true_speed = math.sqrt(true_vel[0]**2 + true_vel[1]**2)
            
            print(f"\nTrue velocities (for comparison):")
            print(f"  True speed:         {true_speed:8.3f} pixels/second")
            print(f"  True angular speed: {true_ang_vel:8.3f} rad/second")
            
            # Note: To convert from timestep to second, divide by FRAME_RATE
            from place_bot.simulation.utils.constants import FRAME_RATE
            linear_speed_per_sec = linear_speed / FRAME_RATE
            angular_speed_per_sec = angular_speed / FRAME_RATE
            print(f"\nConverted to per-second units:")
            print(f"  Estimated linear:  {linear_speed_per_sec:8.3f} pixels/second")
            print(f"  Estimated angular: {angular_speed_per_sec:8.3f} rad/second")
        
        print("="*70)


class MyWorldVelocity(WorldAbstract):
    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (800, 600)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        self._robot_pos = ((-200, 0), 0)
        self._playground.add(robot, self._robot_pos)


def main():
    print("\n" + "="*70)
    print("VELOCITY ESTIMATION FROM ODOMETER EXAMPLE")
    print("="*70)
    print("\nThis example demonstrates velocity estimation from the odometer.")
    print("\nKey concepts:")
    print("- estimated_linear_speed() returns distance per timestep (pixels/timestep)")
    print("- estimated_angular_speed() returns rotation per timestep (rad/timestep)")
    print("- estimated_velocity() returns both in a tuple")
    print("- These values come from the raw odometer displacement (dist, theta)")
    print("- Values include noise like a real odometer sensor")
    print("\nThe robot will:")
    print("  Phase 0: Accelerate")
    print("  Phase 1: Move at constant speed")
    print("  Phase 2: Turn while moving")
    print("\nVelocity information is printed every 20 steps.")
    print("\nPress Q to quit")
    print("="*70 + "\n")
    
    my_robot = MyRobotVelocity()
    my_world = MyWorldVelocity(robot=my_robot)

    simulator = Simulator(the_world=my_world,
                          enable_visu_noises=False,
                          use_keyboard=False)
    simulator.run()


if __name__ == '__main__':
    main()

