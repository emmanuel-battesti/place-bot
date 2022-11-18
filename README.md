


# Table of Content

- [Welcome to *place-bot*](#welcome-to--place-bot-)
- [Simple-Playgrounds](#simple-playgrounds)
- [Installation on Ubuntu](#installation-on-ubuntu)
- [Installation on Windows 10](#installation-on-windows-10)
- [Elements of the environment](#elements-of-the-environment)
- [Programming](#programming)
- [Contact](#contact)

# Welcome to *place-bot*


*Place-bot* is the environment that simulates a robot and his sensors.

[Access to the GitHub repository *Place-bot*](https://github.com/emmanuel-battesti/place-bot)

# Simple-Playgrounds 

This program *Place-bot* is an extension of the *Simple-Playgrounds* (SPG) software library: [https://github.com/mgarciaortiz/simple-playgrounds](https://github.com/mgarciaortiz/simple-playgrounds). However, in the current installation of *Place-bot*, it is the branch *place-bot* of a fork of *Simple-Playgrounds* that is used: [https://github.com/emmanuel-battesti/simple-playgrounds](https://github.com/emmanuel-battesti/simple-playgrounds).


It is recommended to read the [documentation of *Simple-Playgrounds*](https://github.com/emmanuel-battesti/simple-playgrounds#readme).

*Simple-Playgrounds* is an easy-to-use, fast and flexible simulation environment. It bridges the gap between simple and efficient grid environments, and complex and challenging 3D environments. It proposes a large diversity of environments for embodied robots learning through physical interactions. The playgrounds are 2D environments where robots can move around and interact with scene elements.

The game engine, based on [Pymunk](http://www.pymunk.org) and [Arcade](https://api.arcade.academy/), deals with simple physics, such as collision and friction. Robots can act through continuous movements and discrete interactive actions. They perceive the scene with realistic first-person view sensors, top-down view sensors, and semantic sensors.

## Game Engine

In *Simple-Playgrounds*, the game engine used is *Arcade*. Robot enters a Playground, and starts acting and perceiving within this environment. The perception/action/communication loop is managed by the game engine. At each time step, all perception is acquired. Then according to actions to do, robot is moved. Everything is synchronized, unlike what you would get on a real robot.

## Physics Engine

In *Simple-Playgrounds*, the 2d physics library *Pymunk* is used. The physic engine deals with simple physics, such as collision and friction. This gives a mass and inertia to all objects.

# Installation on Ubuntu

This installation procedure has been tested with Ubuntu 18.04 and 20.04.

## Arcade library dependencies

First, you will obviously have to use the Git tool.

And for the library *Arcade*, you might need to install *libjpeg-dev* and *zlib1g-dev*.

```bash
sudo apt update
sudo apt install git libjpeg-dev zlib1g-dev
```

## *Python* installation

We need, at least, *Python 3.8*.

- On *Ubuntu 20.04*, the default version of *Python* is 3.8.
- On *Ubuntu 18.04*, the default version of *Python* is 2.7.17. And the default version of *Python3* is 3.6.9.

But it is easy to install *Python* 3.8:
```bash
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev
```

## *Pip* installation

- Install *Pip*:

```bash
sudo apt update
sudo apt install python3-pip 

- When the installation is complete, verify the installation by checking the *Pip* version:

```bash
pip3 --version
```

- It can be useful to upgrade *Pip* to have the last version in local directory:

```bash
/usr/bin/python3.8 -m pip install --upgrade pip
```

To use the correct version, you have to use `python3.8 -m pip` instead of `pip`, for example:

```bash
python3.8 -m pip --version
```

## Virtual environment tools

The safe way to work with *Python* is to create a virtual environment around the project.

For that, you should install some tools:

```bash
sudo apt update
sudo apt install virtualenvwrapper
```
## Install this *place-bot* repository

- To install this git repository, go to the directory you want to work in (for example: *~/code/*).

- Git-clone the code of [*Place-bot*](https://github.com/emmanuel-battesti/place-bot):

```bash
git clone https://github.com/emmanuel-battesti/place-bot.git
```
This command will create the directory *place-bot* with all the code inside it.

- Create your virtual environment. This command will create a directory *env* where all dependencies will be installed:

```bash
cd place-bot
python3.8 -m venv env
```

- To use this newly create virtual environment, as each time you need it, use the command:

```bash
source env/bin/activate
```

To deactivate this virtual environment, simply type: `deactivate`

- With this virtual environment activated, we can install all the dependency with the command:

```bash
python3.8 -m pip install --upgrade pip
python3.8 -m pip install -r requirements.txt
```

- To test, you can launch:

```bash
python3.8 ./src/place_bot/launcher.py
```

## Python IDE

Although not mandatory, it is a good idea to use an IDE to code in *Python*. It makes programming easier.

For example, you can use the free *community* version of [*PyCharm*](https://www.jetbrains.com/pycharm/). In this case, you have to set your *interpreter* path to your venv path to make it work. 


# Installation on Windows 10

This installation procedure has been tested with Windows 10. Installation is also straightforward on Windows 11.

## *Python* installation

- Open this link in your web browser:  https://www.python.org/downloads/windows/
- Don't choose the lastest version of Python, but choose the 3.8 version. Currently (11/2022), it is the "*Python 3.8.10 - May 3, 2021*".
- For modern machine, you have to choose the *Windows x86-64 executable installer*.
- Once the installer is downloaded, run the Python installer.
- **Important** : you should check the "**Add Python 3.8 to path**"  check box to include the interpreter in the execution path.

## *Git* installation

Git is a tool for source code management. [Git is used](https://www.simplilearn.com/tutorials/git-tutorial/what-is-git "Git is used") to tracking changes in the source code of *place-bot*.

 - Download the [latest version of    Git](https://git-scm.com/download/win) and choose the 64/32 bit version.
 - After the file is downloaded, install it in the system.
 - Once installed, select *Launch the Git Bash*, then click on *finish*. The *Git Bash* is now launched.

We want to work later on the project by using the *Git Bash* terminal.

## Configure *Git Bash*

- Launch the *Git Bash* terminal
- **Warning**, you are **not** by default to your home directory. So to go there, just type : *cd*
- To facilitate the use of the command *python*, you have to create an alias to real position of the program python.exe : `echo "alias python='winpty python.exe'" >> ~/.bashrc`
- Then `source .bashrc` to activate the modification.
- If things are working, the command `python -V` should give the version of the python installed, for example: `Python 3.8.10`

## Install this *place-bot* repository

- To install this git repository, go to the directory you want to work in (for example: *~/code/*).
- With *Git Bash*, you have to use the linux command, for example:
```bash
cd
mkdir code
cd code
```
- Git-clone the code of [*Place-bot*](https://github.com/emmanuel-battesti/place-bot):

```bash
git clone https://github.com/emmanuel-battesti/place-bot.git
```
This command will create the directory *place-bot* with all the code inside it.

- Create your virtual environment. This command will create a directory *env* where all dependencies will be installed:

```bash
cd place-bot
python -m venv env
```

- To use this newly create virtual environment, as each time you need it, use the command:

```bash
source env/Scripts/activate
```

To deactivate this virtual environment, simply type: `deactivate`

- With this virtual environment activated, we can install all the dependency with the command:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- To test, you can launch:

```bash
python ./src/place_bot/launcher.py
```

# Elements of the environment

## Robot

Robot is a version of what is called **agent** in *Simple-Playgrounds*.
Robot is composed of different body parts attached to a *Base*.

Robot **perceives his surroundings** through a first-person view sensor : the *Lidar* sensor.

Robot is equipped with sensors that allow it to **estimate its position and orientation**. We have two kinds:
- with absolute measurements: the *GPS* for the positions and the magnetic *compass* for the orientation.
- with relative measurements: the odometer which provides us with positions and orientation relative to the previous position of the robot.

### Lidar sensor

In the code, class *RobotLidar*.

It emulates a lidar.

- *fov* (field of view): 360 degrees
- *resolution* (number of rays): 181
- *max range* (maximum range of the sensor): 300 pixels

A gaussian noise has been added to the distance.
As the *fov* is 360°, the first (at -Pi rad) and the last value (at Pi) should be the same.

To visualize lidar sensor data, you should set the parameter *draw_lidar* parameter of the *GuiSR* class to *True*.

### GPS sensor

In the file *src/place_bot/spg_overlay/entities/robot_sensors.py*, it is described in the class *RobotGPS*.

This sensor gives the position vector along the horizontal axis and vertical axis.
The position (0, 0) is at the center of the map.
Noise has been added to the data to make it look like GPS noise. This is not just gaussian noise but noise that follows an autoregressive model of order 1.

If you want to enable the visualization of the noises, you should set the parameter *enable_visu_noises* to *True*.

### Compass sensor

In the file *src/place_bot/spg_overlay/entities/robot_sensors.py*, it is described in the class *RobotCompass*.

This sensor gives the orientation of the robot.
The orientation increases with a counter-clockwise rotation of the robot. The value is between -Pi and Pi. 
Noise has been added to the data to make it look like Compass noise. This is not just gaussian noise but noise that follows an autoregressive model of order 1.

If you want to enable the visualization of the noises, you should set the parameter *enable_visu_noises* to *True*.

### Odometer sensor

In the file *src/place_bot/spg_overlay/entities/robot_sensors.py*, it is described in the class *RobotOdometer*.

This sensor returns an array of data containing:
- dist_travel, the distance of the robot's movement during the last timestep.
- alpha, the relative angle of the current position with respect to the previous reference frame of the robot
- theta, the orientation variation (or rotation) of the robot during the last step in the reference frame
     
Those data are relative the previous position of the robot. Usually, we use odometry by integrating measurements over time to get an estimate of the current position of the robot. 
This can be very useful for example when GPS data is no longer provided in some areas of the map.

Angles, alpha and theta, increase with a counter-clockwise rotation of the robot. Their value is between -Pi and Pi. 
Gaussian noise was added separately to the three parts of the data to make them look like real noise. 

![odometer values](img/odom.png)

If you want to enable the visualization of the noises, you should set the parameter *enable_visu_noises* to *True*. It will show also a demonstration of the integration of odometer values, by drawing the estimated path.

### Actuators

At each time step, you must provide values for your actuators.

You have 2 values to move your robot:
- *forward_controller*, a float value between -1 and 1. This is a force apply to your robot in the longitudinal way.
- *angular_vel_controller*, a float value between -1 and 1. This is the speed of rotation. 

You can find examples of actuator use in almost all files in *examples/* and *solutions/*.

## Playground

Robot act and perceive in a *Playground*.

A *playground* is composed of scene elements, which can be fixed or movable. 
The playground with all its elements, except for the robot, are called "Map" within this *Place-bot* repository.

### Coordinate System

A playground is described using a Cartesian coordinate system.

Each element has a position (x,y, theta), with x along the horizontal axis, y along the vertical axis, and theta the orientation in radians, aligned on the horizontal axis. The position (0, 0) is at the center of the map. The value of theta is between -Pi and Pi. Theta increases with a counter-clockwise rotation of the robot. For theta = 0, the robot is oriented towards the right. A playground has a size [width, height], with the width along x-axis, and height along y-axis.


# Programming

## Architecture of *Place-bot*

### file *launcher.py*

*launcher.py* is the main program file to launch a robot using your code.

It will launch the robot that you will have customized in the map that you want, make it run.

This file needs almost no modification to work, except those lines at the beginning of the file:

```python
class MyMap(MyMapComplete01):
    pass


class MyRobot(MyAwesomeRobot):
    pass
```

*MyMap* must inherit from the class of the map you want to use (here, in the example *MyMapComplete01*). This map will be located in the folder *maps*.

*MyRobot* must inherit from the class of the robot that you created (here, in the example, your awesome robot *MyAwesomeRobot*). This robot will be located in the folder *solutions*.

### directory *spg_overlay*

As its name indicates, this folder is a software overlay of the spg (simple-playground) code.
 It contains three sub-directories:
 - *entities*: contains description of differents entities used in the program.
- *gui_map*: contains description of default map and the gui interface.
- *utils*: contains various functions and useful tools.

The files it contains must *not* be modified. It contains the definition of the class *Robot*, of the class of the sensors, etc.

An important file is the *gui_map/gui_sr.py* which contains the class *GuiSR*. 
If you want to use the keyboard to move the first robot, you should set the parameter *use_keyboard* to *True*.
If you want to enable the visualization of the noises, you should set the parameter *enable_visu_noises* to *True*. It will show also a demonstration of the integration of odometer values, by drawing the estimated path.

### directory *maps*

This directory contains the maps in which the robot can move. New maps may appear for new missions with the updates of this repository. You can also make your own maps based on existing ones.

Each map must inherit from the class *MapAbstract*.

### directory *solutions*

This repository will contain your solutions. Taking inspiration from what is there and going beyond, you will put in the code that will define your robot and how it interacts with their environment.

Each Robot must inherit from the class *RobotAbstract*. You have one mandatory member functions: **control()** that will give the action to do for each time step.

For your calculation in the control() function, it is mandatory to use only the sensor without directly accessing the class members. In particular, you should not use the *position* and *angle* variables, but use the *measured_gps_position()* and *measured_compass_angle()* functions to have access to the position and orientation of the robot. These values are noisy, representing more realistic sensors, and can be altered by special zones in the map where the position information can be scrambled.

The true position of the robot can be accessed with the functions *true_position()* and *true_angle()* (or directly with the variable *position* and *angle*), BUT it is only for debugging or logging.

Some examples are provided:
- *my_robot_random.py* shows the actuators

### directory *examples*

In the folder, you will find stand-alone programs to help you program with examples. In particular:
- *display_lidar.py* shows a visualization of the lidar on a graph. You can see the noise added.
- *example_keyboard.py* shows how to use the keyboard for development or debugging purpose. The usable keyboard keys :
	- up / down key : forward and backward
	- left / right key : turn left / right
	- l key : display (or not) the lidar sensor
	- q key : exit the program
	- r key : reset

### directory *tools*

In this directory, you may find some tools... For example, the program *image_to_map.py* allows to build a map from a black and white image.

## Submission

At the end of the course, you will have to submit your solution to your teacher. The teacher will have this same software to evaluate your solution.

Be careful, you will provide only:
- the code to run your simulated robot, which will only come from the *solutions* directory,
- the list of new dependencies needed to make your robot work.

## Various tips

- To exit elegantly after launching a map, press 'q'.

# Contact

If you have questions about the code, you can contact:
emmanuel . battesti at ensta-paris . fr

