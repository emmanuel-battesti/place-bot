"""
Unit tests for RobotAbstract and RobotAbstractDisplayLidar classes.
"""
import math
import numpy as np
import pytest

from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.robot.robot_abstract_display_lidar import RobotAbstractDisplayLidar
from place_bot.simulation.robot.exceptions import DisabledFunctionError
from place_bot.simulation.ray_sensors.lidar import LidarParams
from place_bot.simulation.robot.odometer import OdometerParams


class TestRobot(RobotAbstract):
    """Test implementation of RobotAbstract."""
    
    def control(self):
        return {"forward": 0.0, "rotation": 0.0}


class TestRobotWithDisplay(RobotAbstractDisplayLidar):
    """Test implementation of RobotAbstractDisplayLidar."""
    
    def control(self):
        return {"forward": 0.0, "rotation": 0.0}


def test_robot_initialization():
    """Test that robot initializes correctly with default parameters."""
    robot = TestRobot()
    assert robot is not None
    assert robot.lidar() is not None
    assert not robot.lidar_is_disabled()
    assert not robot.odometer_is_disabled()


def test_robot_with_custom_lidar_params():
    """Test robot initialization with custom lidar parameters."""
    custom_params = LidarParams()
    custom_params.fov = 180
    custom_params.resolution = 181
    custom_params.max_range = 300
    
    robot = TestRobot(lidar_params=custom_params)
    assert robot.lidar().fov_deg() == 180
    assert robot.lidar().resolution == 181


def test_disabled_position_property():
    """Test that accessing position property raises DisabledFunctionError."""
    robot = TestRobot()
    with pytest.raises(DisabledFunctionError) as exc_info:
        _ = robot.position
    assert "odometer_values" in str(exc_info.value) or "true_position" in str(exc_info.value)


def test_disabled_angle_property():
    """Test that accessing angle property raises DisabledFunctionError."""
    robot = TestRobot()
    with pytest.raises(DisabledFunctionError) as exc_info:
        _ = robot.angle
    assert "odometer_values" in str(exc_info.value) or "true_angle" in str(exc_info.value)


def test_disabled_velocity_property():
    """Test that accessing velocity property raises DisabledFunctionError."""
    robot = TestRobot()
    with pytest.raises(DisabledFunctionError) as exc_info:
        _ = robot.velocity
    assert "estimated_linear_speed" in str(exc_info.value) or "estimated_velocity" in str(exc_info.value)


def test_disabled_angular_velocity_property():
    """Test that accessing angular_velocity property raises DisabledFunctionError."""
    robot = TestRobot()
    with pytest.raises(DisabledFunctionError) as exc_info:
        _ = robot.angular_velocity
    assert "estimated_angular_speed" in str(exc_info.value) or "estimated_velocity" in str(exc_info.value)


def test_lidar_ray_angles():
    """Test that lidar ray angles are properly computed."""
    robot = TestRobot()
    angles = robot.lidar_rays_angles()
    
    assert isinstance(angles, np.ndarray)
    assert len(angles) == 361  # Default resolution
    assert angles[0] == pytest.approx(-math.pi, abs=0.01)
    assert angles[-1] == pytest.approx(math.pi, abs=0.01)


def test_lidar_values_initially_none():
    """Test that lidar values are None before first computation."""
    robot = TestRobot()
    # Before any playground step, sensor values might be None or default
    values = robot.lidar_values()
    # We just check it doesn't crash
    assert values is None or isinstance(values, np.ndarray)


def test_odometer_values_initially_none():
    """Test that odometer values are None before first computation."""
    robot = TestRobot()
    # Before any playground step, sensor values might be None or default
    values = robot.odometer_values()
    # We just check it doesn't crash
    assert values is None or isinstance(values, np.ndarray)


def test_control_method_exists():
    """Test that control method can be called."""
    robot = TestRobot()
    command = robot.control()
    assert isinstance(command, dict)
    assert "forward" in command
    assert "rotation" in command


def test_robot_display_lidar_no_display():
    """Test robot with display disabled."""
    robot = TestRobotWithDisplay(should_display_lidar=False)
    assert robot is not None
    # Should not crash when display is called
    robot.display()


def test_lidar_get_ray_angles():
    """Test the new get_ray_angles method."""
    robot = TestRobot()
    angles = robot.lidar().get_ray_angles()
    
    assert isinstance(angles, np.ndarray)
    assert len(angles) > 0
    # Check that angles are within expected range
    assert np.all(angles >= -math.pi)
    assert np.all(angles <= math.pi)


def test_estimated_linear_speed():
    """Test estimated linear speed from odometer."""
    robot = TestRobot()
    speed = robot.estimated_linear_speed()

    # Should return a number (int or float)
    assert isinstance(speed, (int, float))
    # Initially should be 0.0 or very small
    assert speed >= 0.0


def test_estimated_angular_speed():
    """Test estimated angular speed from odometer."""
    robot = TestRobot()
    ang_speed = robot.estimated_angular_speed()

    # Should return a number (int or float)
    assert isinstance(ang_speed, (int, float))


def test_estimated_velocity():
    """Test estimated velocity (both linear and angular)."""
    robot = TestRobot()
    linear, angular = robot.estimated_velocity()

    # Should return a tuple of two numbers
    assert isinstance(linear, (int, float))
    assert isinstance(angular, (int, float))
    assert linear >= 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

