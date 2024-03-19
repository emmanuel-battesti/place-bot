# Table of Content

- [Fast installation on Ubuntu](#fast-installation-on-ubuntu)
- [Detailed installation on Ubuntu](#detailled-installation-on-ubuntu)
- [Detailed installation on Windows 10](#detailled-installation-on-windows-10)

# Fast installation on Ubuntu

## The first time : install dev tools

You can use python version 3.8, 3.9 or 3.10.
 
```bash
sudo apt update -y
sudo apt install -y git libjpeg-dev zlib1g-dev python3 python3-venv python3-dev python3-pip virtualenvwrapper
```

## Installation and launch of the code

```bash
git clone https://github.com/emmanuel-battesti/place-bot.git
cd place-bot
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
python3 ./examples/example.py
```

# Detailed installation on Ubuntu

This installation procedure has been tested with Ubuntu 18.04, 20.04 and 22.04.

## Arcade library dependencies

First, you will obviously have to use the Git tool.

And for the library *Arcade*, you might need to install *libjpeg-dev* and *zlib1g-dev*.

```bash
sudo apt update
sudo apt install git libjpeg-dev zlib1g-dev
```

## *Python* installation

We need, at least, *Python 3.8*. You can use python version 3.8, 3.9 or 3.10.

- On *Ubuntu 22.04*, the default version of *Python* is 3.10.
- On *Ubuntu 20.04*, the default version of *Python* is 3.8.
- On *Ubuntu 18.04*, the default version of *Python* is 2.7.17. And the default version of *Python3* is 3.6.9.

If necessary, it is easy to install *Python* 3.8:
```bash
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-dev
```

## *Pip* installation

- Install *Pip*:

```bash
sudo apt update
sudo apt install python3-pip
```

- When the installation is complete, verify the installation by checking the *Pip* version:

```bash
pip3 --version
```
For Ubuntu 20.04, it returns :
```bash
pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
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

- Git-clone the code of [*place-bot*](https://github.com/emmanuel-battesti/place-bot):

```bash
git clone https://github.com/emmanuel-battesti/place-bot.git
```
This command will create the directory *place-bot* with all the code inside it.

- Create your virtual environment. This command will create a directory *env* where all dependencies will be installed:

```bash
cd place-bot
python3 -m venv env
```

- To use this newly create virtual environment, as each time you need it, use the command:

```bash
source env/bin/activate
```

To deactivate this virtual environment, simply type: `deactivate`

- With this virtual *environment activated*, we can install all the dependency with the command:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

- To test, we can launch an example from the folder examples. Before that, the library have to be installed with the command :

```bash
python3 -m pip install -e . # for a editable installation (or "development mode")
```
or
```bash
python3 -m pip install . # for a normal installation inside the virtual environment
```

- Then, you can launch an example:

```bash
python3 ./examples/example.py
```

## Python IDE

Although not mandatory, it is a good idea to use an IDE to code in *Python*. It makes programming easier.

For example, you can use the free *community* version of [*PyCharm*](https://www.jetbrains.com/pycharm/), or [*Visual Studio Code*](https://code.visualstudio.com/). In this case, you have to set your *interpreter* path to your venv path to make it work.

# Detailed installation on Windows 10

This installation procedure has been tested with Windows 10. Installation is also straightforward on Windows 11.

It would be tempting to install the program with WSL on Windows 10 (Ubuntu console), but this does not work because the program uses shaders with opengl and there is a version problem.

## *Python* installation

- Open this link in your web browser:  https://www.python.org/downloads/windows/
- Don't choose the latest version of Python, but choose the 3.8 version. Currently (11/2022), it is the ["*Python 3.8.10 - May 3, 2021*"](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe).
- For modern machine, you have to choose the *Windows x86-64 executable installer*.
- Once the installer is downloaded, run the Python installer.
- **Important** : you should check the "**Add Python 3.8 to path**"  check box to include the interpreter in the execution path.

## *Git* installation

Git is a tool for source code management. [Git is used](https://www.simplilearn.com/tutorials/git-tutorial/what-is-git "Git is used") to tracking changes in the source code of *place-bot*.

 - Download the [latest version of    Git](https://git-scm.com/download/win) and choose the 64/32 bit version.
 - After the file is downloaded, install it in the system with the default options.
 - Once installed, select *Launch the Git Bash*, then click on *finish*. The *Git Bash* is now launched.

We want to work later on the project by using the *Git Bash* terminal.

## Configure *Git Bash*

- Launch the *Git Bash* terminal
- **Warning**, you are **not** by default to your home directory. So to go there, just type : *cd*
- To facilitate the use of the command *python*, you have to create an alias to real position of the program python.exe : `echo "alias python='winpty python.exe'" >> ~/.bashrc`
- Then `source .bashrc` to activate the modification.
- If things are working, the command `python -V` should give the version of the python installed, for example: `Python 3.8.10`

## Install this *place-bot* repository

- To install this git repository, we create a new directory where you will work in (for example: *~/code/*).
- With *Git Bash*, you have to use the linux command, for example:
```bash
cd
mkdir code
cd code
```
- Git-clone the code of [*place-bot*](https://github.com/emmanuel-battesti/place-bot):

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

Later, if you need it, to deactivate this virtual environment, simply type: `deactivate`

- With this virtual environment activated, we can install all the dependency with the command:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

- To test, we can launch an example from the folder examples. Before that, the library have to be installed with the command :

```bash
python -m pip install -e . # for a editable installation (or "development mode")
```
or
```bash
python -m pip install . # for a normal installation inside the virtual environment
```

- Then, you can launch an example:

```bash
python ./examples/example.py
```
