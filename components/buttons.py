# components/buttons.py
"""
Custom button components for the application
"""

from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation

class PrimaryButton(Button):
    """Primary button with clean, modern styling"""

    def __init__(self, **kwargs):
        # Set up the button with clean defaults
        super().__init__(**kwargs)

        # Clean visual setup
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0.863, 0.078, 0.235, 1]  # Crimson Red #DC143C
        self.color = [1, 1, 1, 1]  # White text
        self.bold = True

        # Let KV file control sizing completely
        # Only set minimal defaults if nothing specified
        if not hasattr(self, 'font_size') or self.font_size == 15:  # Kivy's default
            self.font_size = 16
        if not hasattr(self, 'padding'):
            self.padding = (16, 8)

        # Bind press/release animations
        self.bind(on_press=self._on_press_animation)
        self.bind(on_release=self._on_release_animation)

    def _on_press_animation(self, instance):
        """Smooth press animation"""
        from kivy.animation import Animation
        anim = Animation(opacity=0.7, duration=0.1)
        anim.start(self)

    def _on_release_animation(self, instance):
        """Smooth release animation"""
        from kivy.animation import Animation
        anim = Animation(opacity=1.0, duration=0.15)
        anim.start(self)

class DiceButton(Button):
    """Specialized button for dice selection with clean, modern styling"""

    dice_type = NumericProperty(0)  # Number of sides

    def __init__(self, **kwargs):
        # Extract our custom properties before calling super()
        dice_type = kwargs.pop('dice_type', 0)

        # Set up the button with clean defaults
        super().__init__(**kwargs)

        # Set our custom property
        self.dice_type = dice_type

        # Clean visual setup - only set if not already set by KV
        if not hasattr(self, 'background_normal') or self.background_normal == '':
            self.background_normal = ''
        if not hasattr(self, 'background_down') or self.background_down == '':
            self.background_down = ''
        if not hasattr(self, 'background_color') or self.background_color == [1, 1, 1, 1]:
            self.background_color = [0.863, 0.078, 0.235, 1]  # Crimson red (same as PrimaryButton)
        if not hasattr(self, 'color') or self.color == [1, 1, 1, 1]:
            self.color = [1, 1, 1, 1]  # White text (same as PrimaryButton)
        if not hasattr(self, 'bold') or not self.bold:
            self.bold = True

        # Only set font_size if not specified in KV
        if not hasattr(self, 'font_size') or self.font_size == 15:  # Kivy's default
            self.font_size = 16

        # Bind press/release animations
        self.bind(on_press=self._on_press_animation)
        self.bind(on_release=self._on_release_animation)

    def _on_press_animation(self, instance):
        """Smooth press animation"""
        from kivy.animation import Animation
        anim = Animation(opacity=0.7, duration=0.1)
        anim.start(self)

    def _on_release_animation(self, instance):
        """Smooth release animation"""
        from kivy.animation import Animation
        anim = Animation(opacity=1.0, duration=0.15)
        anim.start(self)