import arcade


class KeyboardController:
    """
    The KeyboardController class is responsible for handling keyboard input and
    converting it into commands for controlling a robot. It keeps track of the
    current command values for forward movement and rotation.
    """

    def __init__(self):
        # A dictionary that stores the current command values for forward movement and rotation.
        self._command = {"forward": 0.0,
                         "rotation": 0.0}

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Updates the command values based
        on the pressed key."""
        if self._command:

            if key == arcade.key.UP:
                self._command["forward"] = 1.0
            elif key == arcade.key.DOWN:
                self._command["forward"] = -1.0

            if key == arcade.key.LEFT:
                self._command["rotation"] = 1.0
            elif key == arcade.key.RIGHT:
                self._command["rotation"] = -1.0

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released. Resets the command values based
        on the released key."""
        if self._command:

            if key == arcade.key.UP:
                self._command["forward"] = 0
            elif key == arcade.key.DOWN:
                self._command["forward"] = 0

            if key == arcade.key.LEFT:
                self._command["rotation"] = 0
            elif key == arcade.key.RIGHT:
                self._command["rotation"] = 0

    def control(self):
        """Returns the current command values."""
        return self._command
