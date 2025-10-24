import time
from typing import Optional, Tuple, Dict, Union, Type

import arcade
import cv2

from place_bot.simulation.robot.controller import Command, Controller
from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.gui_map.keyboard_controller import KeyboardController
from place_bot.simulation.gui_map.world_abstract import WorldAbstract
from place_bot.simulation.gui_map.top_down_view import TopDownView
from place_bot.simulation.reporting.screen_recorder import ScreenRecorder
from place_bot.simulation.utils.constants import FRAME_RATE, ENABLE_WINDOW_AUTO_RESIZE
from place_bot.simulation.utils.fps_display import FpsDisplay
from place_bot.simulation.utils.mouse_measure import MouseMeasure
from place_bot.simulation.utils.visu_noises import VisuNoises
from place_bot.simulation.utils.window_utils import auto_resize_window


class Simulator(TopDownView):
    """
    The Simulator class is a subclass of TopDownView and provides a graphical user
    interface for the simulation. It handles the rendering of the playground,
    robot, and other visual elements, as well as user input and interaction.
    """


    def _handle_window_auto_resize(self, the_world: WorldAbstract, size: Optional[Tuple[int, int]],
                                  zoom: float, headless: bool) -> Tuple[Optional[Tuple[int, int]], float]:
        """
        Handle automatic window resizing for small screens.

        Args:
            the_world: The map object containing the playground
            size: Initial window size
            zoom: Initial zoom factor
            headless: Whether running in headless mode

        Returns:
            Tuple of (adjusted_size, adjusted_zoom)
        """
        # Auto-resize window if needed for small screens (before window creation)
        if not headless and ENABLE_WINDOW_AUTO_RESIZE:
            # If size is None, use the playground size or a default
            if size is None:
                size = the_world.playground.size if the_world.playground.size else (1200, 800)

            # Check if this is a problematic map size that causes rendering issues
            problematic_sizes = [(1660, 1122)]  # MapMedium01 and similar
            is_problematic = size in problematic_sizes

            if not is_problematic:
                # Apply auto-resize with zoom adjustment only for non-problematic maps
                adjusted_size, calculated_zoom = auto_resize_window(size)
                if adjusted_size != size:
                    size = adjusted_size
                    zoom = zoom * calculated_zoom # Apply the calculated zoom factor
            else:
                # For problematic maps, disable auto-resize completely
                # Let the user handle window size manually or use system defaults
                print(f"Auto-resize désactivé pour cette carte ({size[0]}x{size[1]})")
        elif not headless and not ENABLE_WINDOW_AUTO_RESIZE:
            # Auto-resize is globally disabled
            if size is None:
                size = the_world.playground.size if the_world.playground.size else (1200, 800)
            print("Auto-resize désactivé globalement via ENABLE_WINDOW_AUTO_RESIZE")

        return size, zoom

    def __init__(
            self,
            the_world: WorldAbstract,
            size: Optional[Tuple[int, int]] = None,
            center: Tuple[float, float] = (0, 0),
            zoom: float = 1,
            use_keyboard: bool = False,
            use_color_uid: bool = False,
            draw_transparent: bool = False,
            draw_interactive: bool = False,
            draw_lidar_rays: bool = False,
            use_mouse_measure: bool = False,
            enable_visu_noises: bool = False,
            filename_video_capture: str = None,
            headless: bool = False,
    ) -> None:
        """
        Initialize the Simulator graphical user interface.

        Args:
            the_world (WorldAbstract): The map object containing the playground and robot.
            size (Optional[Tuple[int, int]]): Size of the window.
            center (Tuple[float, float]): Center of the view.
            zoom (float): Zoom factor.
            use_keyboard (bool): Enable keyboard control for the first robot.
            use_color_uid (bool): Use color UID for sprites.
            draw_transparent (bool): Draw transparent sprites.
            draw_interactive (bool): Draw interactive sprites.
            draw_lidar_rays (bool): Draw lidar sensor rays.
            use_mouse_measure (bool): Enable mouse measurement tool.
            enable_visu_noises (bool): Enable visualization of sensor noises.
            filename_video_capture (str): Output filename for video capture.
        """
        # Handle automatic window resizing
        size, zoom = self._handle_window_auto_resize(the_world, size, zoom, headless)

        super().__init__(
            the_world.playground,
            size,
            center,
            zoom,
            use_color_uid,
            draw_transparent,
            draw_interactive,
        )


        self._headless = headless
        self._playground.window.set_size(*self._size)

        self._the_world = the_world
        self._robot = self._the_world.robot

        self._robot_commands: Union[Dict[RobotAbstract, Dict[Union[str, Controller], Command]], Type[None]] = None
        if self._robot:
            self._robot_commands = {}

        # image_icon = pyglet.resource.image("resources/robot_v2.png")
        # self._playground.window.set_icon(image_icon)
        # Ok for the first round, crash for the second round ! I dont know
        # why...

        self._playground.window.set_visible(not self._headless)
        self._playground.window.headless = self._headless

        self._playground.window.on_draw = self.on_draw
        self._playground.window.on_update = self.on_update
        self._playground.window.on_key_press = self.on_key_press
        self._playground.window.on_key_release = self.on_key_release
        self._playground.window.on_mouse_motion = self.on_mouse_motion
        self._playground.window.on_mouse_press = self.on_mouse_press
        self._playground.window.on_mouse_release = self.on_mouse_release
        self._playground.window.set_update_rate(FRAME_RATE)

        self._use_keyboard = use_keyboard

        self._draw_lidar_rays = draw_lidar_rays
        self._use_mouse_measure = use_mouse_measure
        self._enable_visu_noises = enable_visu_noises

        self._elapsed_timestep = 0
        self._start_timestamp = time.time()
        self._elapsed_walltime = 0.001

        self._terminate = False

        self.fps_display = FpsDisplay(period_display=2)
        self._keyboardController = KeyboardController()
        self._mouse_measure = MouseMeasure(playground_size=the_world.playground.size)
        self._visu_noises = VisuNoises(playground_size=the_world.playground.size,
                                       robot=self._robot)

        self.recorder = ScreenRecorder(self._size[0], self._size[1], fps=30,
                                       out_file=filename_video_capture)

    def close(self) -> None:
        """
        Close the simulation window.
        """
        self._playground.window.close()

    def set_caption(self, window_title: str) -> None:
        """
        Set the window caption/title.

        Args:
            window_title (str): The title to set.
        """
        self._playground.window.set_caption(window_title)

    def run(self) -> None:
        """
        Start the simulation event loop.
        """
        self._playground.window.run()


    def on_draw(self) -> None:
        """
        Render the current frame to the window.
        """
        # Clear the window
        self._playground.window.clear()
        # Binding the framebuffer object to the window
        # Is it necessary ? It seems to work without it.
        self._fbo.use()

        # Draw the playground and all the entities in it
        # Copier le contenu de draw() ici ?
        self.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Update the simulation state and draw the playground and entities.

        Args:
            delta_time (float): Time since last update.
        """
        self._elapsed_timestep += 1

        if self._elapsed_timestep < 2:
            self._playground.step(all_commands=self._robot_commands)
            return

        # COMPUTE COMMANDS
        self._robot.elapsed_walltime = self._elapsed_walltime
        self._robot.elapsed_timestep = self._elapsed_timestep
        command = self._robot.control()
        if self._use_keyboard:
            command = self._keyboardController.control()

        self._robot_commands[self._robot] = command

        if self._robot and hasattr(self._robot, 'display'):
            self._robot.display()

        self._playground.step(all_commands=self._robot_commands)

        self._visu_noises.update(enable=self._enable_visu_noises)

        last_timestamp = time.time()
        self._elapsed_walltime = last_timestamp - self._start_timestamp

        # Capture the frame
        # Au bon endroit ? Il faudrait le mettre avant le draw() ?
        self.recorder.capture_frame(self)

        self.fps_display.update(display=False)

        if self._terminate:
            self.recorder.end_recording()
            arcade.close_window()

    def get_playground_image(self) -> cv2.typing.MatLike:
        """
        Get the image of the playground in the framebuffer.

        Returns:
            Any: The image as a numpy array.
        """
        self.update_and_draw_in_framebuffer()
        # The image should be flip and the color channel permuted
        image = cv2.flip(self.get_np_img(), 0)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def draw(self, force: bool = False) -> None:
        """
        Draw the playground and all the entities in it in the window.

        Args:
            force (bool): If True, force update of all sprites.
        """
        arcade.start_render()
        self.update_sprites_position(force)

        self._playground.window.use()
        self._playground.window.clear(self._background)

        for robot in self._playground.agents:
            robot.draw_bottom_layer()

        if self._draw_lidar_rays:
            for robot in self._playground.agents:
                robot.lidar().draw()

        self._mouse_measure.draw(enable=self._use_mouse_measure)
        self._visu_noises.draw(enable=self._enable_visu_noises)

        self._transparent_sprites.draw(pixelated=True)
        self._interactive_sprites.draw(pixelated=True)
        self._visible_sprites.draw(pixelated=True)

        for robot in self._playground.agents:
            robot.draw_top_layer()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Called whenever a key is pressed.

        Args:
            key (int): The key code pressed.
            modifiers (int): Modifier keys pressed.
        """
        self._keyboardController.on_key_press(key, modifiers)

        if key == arcade.key.L:
            self._draw_lidar_rays = not self._draw_lidar_rays

        if key == arcade.key.Q:
            self._terminate = True

        if key == arcade.key.R:
            self._playground.reset()
            self._visu_noises.reset()


    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Called whenever a key is released.

        Args:
            key (int): The key code released.
            modifiers (int): Modifier keys pressed.
        """
        self._keyboardController.on_key_release(key, modifiers)

    # Creating function to check the position of the mouse
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """
        Called whenever the mouse is moved.

        Args:
            x (int): X position.
            y (int): Y position.
            dx (int): Change in X.
            dy (int): Change in Y.
        """
        self._mouse_measure.on_mouse_motion(x, y, dx, dy)

    # Creating function to check the mouse clicks
    def on_mouse_press(self, x: int, y: int, button: int, _: int) -> None:
        """
        Called whenever a mouse button is pressed.

        Args:
            x (int): X position.
            y (int): Y position.
            button (int): Mouse button.
            _ (int): Modifier keys pressed.
        """
        self._mouse_measure.on_mouse_press(x, y, button,
                                           enable=self._use_mouse_measure)

    def on_mouse_release(self, x: int, y: int, button: int, _: int) -> None:
        """
        Called whenever a mouse button is released.

        Args:
            x (int): X position.
            y (int): Y position.
            button (int): Mouse button.
            _ (int): Modifier keys pressed.
        """
        self._mouse_measure.on_mouse_release(x, y, button,
                                             enable=self._use_mouse_measure)

    @property
    def elapsed_timestep(self) -> int:
        """
        Returns the number of elapsed timesteps.

        Returns:
            int: Elapsed timesteps.
        """
        return self._elapsed_timestep

    @property
    def elapsed_walltime(self) -> float:
        """
        Returns the elapsed wall time in seconds.

        Returns:
            float: Elapsed wall time.
        """
        return self._elapsed_walltime
