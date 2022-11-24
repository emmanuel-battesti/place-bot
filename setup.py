from os import path

from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

# read the contents of the README file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="place-bot",
    version="0.0",
    description="A simple robot simulator",
    author="Emmanuel Battesti",
    author_email="emmanuel.battesti@ensta-paris.fr",
    url="https://github.com/emmanuel-battesti/place-bot",
    license='MIT',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
