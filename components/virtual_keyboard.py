"""Custom on-screen keyboard for touch devices."""

from __future__ import annotations

from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class _DismissArea(Widget):
    """Transparent area above the keyboard to dismiss it on tap."""

    def __init__(self, controller: "KeyboardController", **kwargs):
        super().__init__(**kwargs)
        self._controller = controller

    def on_touch_down(self, touch):  # noqa: D401 - Kivy signature
        if self.collide_point(*touch.pos):
            self._controller.hide_immediately()
            return True
        return super().on_touch_down(touch)


class OnScreenKeyboard(FloatLayout):
    """Half-screen keyboard overlay anchored to the bottom of the window."""

    def __init__(self, controller: "KeyboardController", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.opacity = 0
        self.disabled = True
        self._controller = controller
        self.target = None  # Active TextInput
        self._shift_active = False
        self._letter_buttons: list[Button] = []

        # Transparent area (top half) to catch taps and dismiss the keyboard
        self._dismiss_area = _DismissArea(controller, size_hint=(1, 0.5), pos_hint={"x": 0, "y": 0.5})
        self.add_widget(self._dismiss_area)

        # Keyboard panel at bottom half
        self._keyboard_panel = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.5),
            pos_hint={"x": 0, "y": 0},
            padding=[12, 12, 12, 20],
            spacing=12,
        )
        self.add_widget(self._keyboard_panel)

        self._build_layout()

    # ------------------------------------------------------------------
    # Layout construction
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        """Create keyboard button layout."""
        rows = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Backspace"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
            ["Shift", "a", "s", "d", "f", "g", "h", "j", "k", "l", "Enter"],
            ["Hide", "Space", "-", "'", ",", "."]
        ]

        for index, row_keys in enumerate(rows):
            row_layout = BoxLayout(spacing=8)
            for key in row_keys:
                btn = Button(
                    text=key.upper() if key.isalpha() else key.capitalize() if key in {"backspace", "shift", "enter", "hide", "space"} else key,
                    size_hint_x=self._size_hint_for_key(key),
                    font_size=24,
                    background_normal="",
                    background_color=(0.2, 0.2, 0.2, 0.95),
                    color=(1, 1, 1, 1),
                    bold=True,
                )
                btn.bind(on_release=partial(self._handle_key_press, key))
                row_layout.add_widget(btn)

                if key.isalpha():
                    self._letter_buttons.append(btn)
            self._keyboard_panel.add_widget(row_layout)

    @staticmethod
    def _size_hint_for_key(key: str) -> float:
        if key == "Space":
            return 3.0
        if key in {"Backspace", "Shift", "Enter", "Hide"}:
            return 1.5
        return 1.0

    # ------------------------------------------------------------------
    # Visibility management
    # ------------------------------------------------------------------
    def open(self) -> None:
        if self.parent is None:
            Window.add_widget(self)
        self.disabled = False
        self.opacity = 1

    def dismiss(self) -> None:
        if self.parent is not None:
            Window.remove_widget(self)
        self.disabled = True
        self.opacity = 0
        self.target = None

    # ------------------------------------------------------------------
    # Target management
    # ------------------------------------------------------------------
    def set_target(self, text_input) -> None:
        self.target = text_input
        self._ensure_focus()

    def clear_target(self) -> None:
        self.target = None
        self._shift_active = False
        self._update_letter_case()

    def _ensure_focus(self) -> None:
        if self.target is None:
            return
        Clock.schedule_once(lambda dt: setattr(self.target, "focus", True), 0)

    # ------------------------------------------------------------------
    # Key handling
    # ------------------------------------------------------------------
    def _handle_key_press(self, key: str, button: Button) -> None:
        target = self.target
        if target is None and key not in {"Hide", "Enter"}:
            return

        if key == "Backspace":
            target.do_backspace(from_undo=False)
        elif key == "Space":
            target.insert_text(" ")
        elif key == "Enter":
            # Confirm input and hide keyboard
            self._controller.hide_immediately(target)
            return
        elif key == "Shift":
            self._toggle_shift()
            return
        elif key == "Hide":
            self._controller.hide_immediately(target)
            return
        else:
            char = key.upper() if self._shift_active else key.lower() if key.isalpha() else key
            target.insert_text(char)

        self._ensure_focus()

    def _toggle_shift(self) -> None:
        self._shift_active = not self._shift_active
        self._update_letter_case()

    def _update_letter_case(self) -> None:
        for btn in self._letter_buttons:
            key = btn.text.lower()
            btn.text = key.upper() if self._shift_active else key.lower()


class KeyboardController:
    """Controls a shared instance of the on-screen keyboard."""

    def __init__(self):
        self._keyboard = OnScreenKeyboard(self)
        self._ignore_focus_loss: set = set()

    def show(self, text_input) -> None:
        self._keyboard.set_target(text_input)
        if self._keyboard.parent is None:
            self._keyboard.open()

    def refocus(self) -> None:
        self._keyboard._ensure_focus()

    def hide_immediately(self, text_input=None) -> None:
        if text_input is None:
            text_input = self._keyboard.target
        if text_input is not None:
            self._ignore_focus_loss.add(text_input)
            if text_input.focus:
                text_input.focus = False
        self._keyboard.dismiss()


    def on_focus_lost(self, text_input) -> None:
        if self._keyboard.target is not text_input:
            return
        if text_input in self._ignore_focus_loss:
            self._ignore_focus_loss.remove(text_input)
            return
        self._keyboard._ensure_focus()

    @property
    def keyboard(self) -> OnScreenKeyboard:
        return self._keyboard


keyboard_controller = KeyboardController()
