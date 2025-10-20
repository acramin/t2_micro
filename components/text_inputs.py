"""Custom TextInput widgets with persistent keyboard support"""

from kivy.uix.textinput import TextInput

from components.virtual_keyboard import keyboard_controller


class PersistentKeyboardTextInput(TextInput):
    """TextInput wired to the custom on-screen keyboard."""

    def on_focus(self, instance, value):  # noqa: D401 - Kivy signature
        parent_on_focus = getattr(super(PersistentKeyboardTextInput, self), "on_focus", None)
        if parent_on_focus:
            parent_on_focus(instance, value)
        if value:
            keyboard_controller.show(self)
        else:
            keyboard_controller.on_focus_lost(self)

    def insert_text(self, substring, from_undo=False):
        super().insert_text(substring, from_undo=from_undo)
        keyboard_controller.refocus()

    def do_backspace(self, from_undo=False, mode='bkspc'):  # noqa: D401
        super().do_backspace(from_undo=from_undo, mode=mode)
        keyboard_controller.refocus()
