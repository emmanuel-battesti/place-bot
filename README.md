# Table of Content

- [Welcome to *Place-Bot*](#welcome-to-place-bot)
- [Simulation Environment](#simulation-environment)
- [Installation](#installation)
- [Elements of the environment](#elements-of-the-environment)
- [Programming Your Robot](#programming-your-robot)
- [Contact](#contact)

# Welcome to *Place-Bot*

*Place-Bot* is the environment that simulates a robot and his sensors.

[Access to the GitHub repository *Place-Bot*](https://github.com/emmanuel-battesti/place-bot)

# Simulation Environment

Place-Bot is built on a modified code of the 2D simulation library [**Simple-Playgrounds**](https://github.com/mgarciaortiz/simple-playgrounds) (SPG), which uses the **Pymunk** physics engine and the **Arcade** game engine.

In practical terms, this means:
- Robots and objects have mass and inertia (they don't stop instantly).
- Collisions are handled by the physics engine.
- The simulator manages a perception-action-communication loop at each time step.

# Installation

For installation instructions, please refer to the [`INSTALL.md`](INSTALL.md) file.

# Elements of the environment

## Robot

Robot is a type of **agent** in *Simple-Playgrounds*.
Robot is composed of different body parts attached to a *Base*.

Robot **perceives his surroundings** through a first-person view sensor : the *Lidar* sensor.

Robot is equipped with an odometry sensor that allow it to **estimate its position and orientation**. The odometer provides us current position and orientation relative to the first position of the robot.

### Lidar sensor

In the file `src/place_bot/simulation/ray_sensors/lidar.py`, class *Lidar*.

It emulates a lidar sensor with the following specifications:

- *fov* (field of view): 360 degrees
- *resolution* (number of rays): 361
- *max range* (maximum range of the sensor): 600 pixels

Gaussian noise has been added to the distance measurements to simulate real-world conditions.
As the *field of view* (fov) is 360°, the first value (at -Pi rad) and the last value (at Pi) should be the same.

To visualize lidar sensor data, you need to set the parameter *draw_lidar_rays* of the *Simulator* class to *True*.

### Odometer sensor

In the file `src/place_bot/simulation/robot/odometer.py`, it is described in the class *Odometer*.

This sensor returns an array of data containing the pose of the robot by integrating its displacement at each step.
Its displacement is :
- `dist_travel`: Distance traveled during the last timestep (in pixels)
- `alpha`: Relative angle of the current position with respect to the previous frame (in radians)
- `theta`: Orientation variation (rotation) during the last timestep (in radians)

Angles, alpha and theta, increase with a counter-clockwise rotation of the robot. Their value is between -Pi and Pi.
Gaussian noise was added separately to the three parts of the data to make them look like real noise.

We use those noisy odometry data by integrating measurements over time to finally get an estimate of the current position of the robot.

If you want to enable the visualization of the noises, you need to set the parameter *enable_visu_noises* parameter of the *Simulator* class constructor to *True*. It will show also a demonstration of the integration of odometer values, by drawing the estimated path.

### Actuators

At each time step, you must provide values for your actuators.

You have 2 values to control your robot's movement:
- *forward*: A float value between -1 and 1. This applies force in the longitudinal direction.
- *rotation*: A float value between -1 and 1. This controls the rotation speed.

You can find examples of actuator use in almost all files in `examples/`.

## Playground

Robot acts and perceives in a *Playground*.

A *playground* is composed of scene elements, which can be fixed or movable.
The playground with all its elements, except for the robot, is called a "World" within this *Place-Bot* repository.

### Coordinate System

The playground uses a standard Cartesian coordinate system:

* The position `(x, y)` :
  - Origin (0,0) is at the center of the world.
  - `x`: Horizontal position (positive values to the right)
  - `y`: Vertical position (positive values upward)

* The orientation `theta`:
  - Measured in radians between -π and π
  - Increases with counter-clockwise rotation
  - At `theta` = 0, the robot faces right (positive x-axis)

* World Dimensions:
  - Worlds have a size [width, height], with width along x-axis and height along y-axis
  - All measurements are in pixels

# Programming Your Robot

## Architecture of *Place-Bot*

### Directory *src/place_bot*

As its name indicates, this folder contains the code of the place_bot simulator.
 It contains several subdirectories:
- *elements*: contains description of different entities used in the program.
- *gui_map*: contains description of default world and the simulator interface.
- *robot*: contains robot-related classes including sensors and controllers.
- *ray_sensors*: contains lidar and distance sensor implementations.
- *utils*: contains various functions and useful tools.
- *reporting*: contains tools for recording and reporting simulation data.

We have also two others directories:
- *resources*: contains the image for the sprite of the robot and the texture of the walls.
- *tools*: contains tools to create complex worlds automatically.

An important file is the *gui_map/simulator.py* which contains the class *Simulator*.
If you want to use the keyboard to move the first robot, you should set the parameter *use_keyboard* to *True*.
If you want to enable the visualization of the noises, you should set the parameter *enable_visu_noises* to *True*. It will show also a demonstration of the integration of odometer values, by drawing the estimated path.

### Directory *examples*

In the `examples/` folder at the root of the repository, you will find stand-alone programs to help you understand key concepts. In particular:
- `example_display_lidar.py` shows a visualization of the lidar on a graph, with noise.
- `example_keyboard.py` shows how to use the keyboard for development or debugging. Usable keys include:
	- up / down key : forward and backward
	- left / right key : turn left / right
	- l key : display (or not) the lidar sensor
	- q key : exit the program
	- r key : reset

### File *examples/example.py*

*examples/example.py* is the main example file to launch a robot using your code.

It will launch the robot that you will have customized in the world that you want, make it run.

This file needs almost no modification to work, except those lines at the beginning of the file:

```python
class MyWorld(MyWorldComplete01):
    pass


class MyRobot(MyAwesomeRobot):
    pass
```

*MyWorld* must inherit from the class of the world you want to use (here, in the example *MyWorldComplete01*). This world will be located in the folder *examples/worlds*.

*MyRobot* must inherit from the class of the robot that you created (here, in the example, your awesome robot *MyAwesomeRobot*). This robot will be located in the folder *examples/robots*.


### Directory *examples/worlds*

This directory `examples/worlds` contains the worlds used by the robot. They are only used here as examples. You can also create your own worlds based on existing ones.

Every world file contains a main function, allowing the file to be executed directly to observe the world. In this case, the world is run with a stationary robot. The parameter `use_mouse_measure` is set to `True` so the measuring tool is active when clicking on the screen.

Each world must inherit from the class *WorldAbstract*.

### Directory *examples/robots*

This directory contains some robots. They are only used here as examples. By taking inspiration from what is there and going beyond it, you will implement the code that will define your robot and the way it interacts with its environment.

Each Robot must inherit from the class *RobotAbstract*. You have one mandatory member functions: **control()** that will give the action to do for each time step.

For your calculation in the control() function, it is mandatory to use only the sensor without directly accessing the class members. In particular, you should not use the *position* and *angle* variables, but you should compute an estimated position and orientation of the robot from the odometry data. These values are noisy, representing more realistic sensors.

The true position of the robot can be accessed with the functions *true_position()* and *true_angle()* (or directly with the variable *position* and *angle*), BUT it is only for debugging or logging.

Some examples are provided:
- *my_robot_random.py* shows the actuators

## Directory *tools*

In `src/place_bot/tools`, you may find utilities to create worlds, make measurements, etc. Notably:
- `image_to_world.py` builds a world from a black and white image.
- `check_world.py` shows a world without robot; clicking prints coordinates—useful for designing or modifying a world.

## Various tips

### Exiting an execution

- To exit elegantly after launching a world, press `Q` in the simulation window (exits current round).
- To exit the entire program immediately, press `E` in the simulation window (exits all rounds).

### Enable some visualizations

The `Simulator` class can be constructed with the following parameters (defaults shown):
- `draw_lidar_rays`: False. Draws lidar rays.
- `use_keyboard`: False.
- `use_mouse_measure`: False. Click to print the mouse position.
- `enable_visu_noises`: False.
- `filename_video_capture`: None to disable; otherwise the output video filename.

### Print FPS performance in the terminal

Display the program's FPS in the console at regular intervals. The FPS display is handled by the `FpsDisplay` class in `src/place_bot/simulation/utils/fps_display.py`. 
The display period can be configured when creating the `Simulator` instance, and FPS information is automatically shown during simulation.

### Show your own display

In *RobotAbstract*, you can override two functions to draw overlays:
- `draw_top_layer()`: draw on top of all layers.
- `draw_bottom_layer()`: draw below all other layers.

These methods allow you to add custom visual elements or debugging information to the simulation display.

### Create a new world

Creating custom worlds is useful to reproduce specific scenarios, stress-test parts of your algorithm, and compare strategies under controlled conditions.

To add a new world you must create and add two files in `examples/worlds`:
- `world_<name>.py` — defines the World class (inherits from `WorldAbstract`). In the `__init__` of your World class paste the initialization lines printed by `image_to_world.py` so the world parameters exactly match the conversion. Implement `build_playground()` to set robot start position and to call helper functions that add walls/boxes.
- `walls_<name>.py` — contains the helper functions generated by `image_to_world.py` (the script writes `generated_code.py`). Copy the generated helper functions (for example `add_walls(playground)` and `add_boxes(playground)`) into `walls_<name>.py` and import them from `world_<name>.py`.

Step-by-step workflow

1. Draw your world as a PNG image with clear, consistent colors:
   - Walls: pure black (RGB 0,0,0), ~10 px thick for robust detection.
2. Edit `img_path` in `src/place_bot/tools/image_to_world.py` to point to your PNG and run the script. The tool is interactive and shows intermediate images with OpenCV (`cv2.imshow`); press any key to advance (`cv2.waitKey(0)`). On success, it will:
   - write a `generated_code.py` that contains helper functions (walls/boxes), and
   - print a few Python initialization lines in the console.
3. Copy the helper functions from `generated_code.py` into a new file `examples/worlds/walls_<name>.py`.
4. COPY the initialization lines printed in the console into the `__init__` of your `World` class in `examples/worlds/world_<name>.py`. Important: copy these exact assignments so your world parameters match the converter output:
   - `self._size_area`
5. Implement `build_playground()` in `world_<name>.py` to:
   - import and call the helper functions from `walls_<name>.py` to add walls/boxes,
   - define robot starting area/position (the converter does not create robot starts automatically),
   - add any return area or extra elements required by your scenario.
6. Validate visually using `src/place_bot/tools/check_world.py` (displays the world without robot and prints coordinates when clicking). After visual validation, run a short simulation to smoke-test the world:

Notes & troubleshooting
- Exact variables to copy: when you run `image_to_world.py` the console output contains the Python lines to paste into your `world_<name>.py`. In particular copy the assignments for `self._size_area` into your World class `__init__`.
- Color detection: `image_to_world.py`.
- Robot start positions: the converter does not set robot starting positions. Add them explicitly in `world_<name>.py` — see existing `world_*.py` examples for idiomatic patterns.
- Small elements and thickness: keep walls reasonably thick in the source PNG (~8–12 px) to avoid fragmentation during detection.
- Final check: after creating both files (`world_<name>.py`, `walls_<name>.py`) and validating with `check_world.py`, run a short simulation to validate the world in situ.

# Getting Started

Welcome to Place-Bot! This section will help you quickly set up and run your first simulation with a custom robot controller.

## Installation

Follow [INSTALL.md](INSTALL.md) to set up your environment, install dependencies, and troubleshoot common issues. Supported platforms include Ubuntu (recommended) and Windows (with WSL2 or Git Bash).

## Quick Start Example

Once installed, you can launch a default simulation with:

```bash
python3 examples/example.py
```


# Contact

If you have questions about the code, propose improvements or report bugs, you can contact:
emmanuel . battesti at ensta . fr

