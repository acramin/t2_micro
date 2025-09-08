# components/buttons.py
"""
Custom button components for the application
"""

from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation

class PrimaryButton(Button):
    """Primary button with custom styling and animations"""
    
    # Custom properties
    bg_color = ListProperty([0.541, 0.169, 0.886, 1])  # #8A2BE2
    text_color = ListProperty([1, 1, 1, 1])
    corner_radius = NumericProperty(8)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.bg_color
        self.color = self.text_color
        self.size_hint = (None, None)
        self.height = 48
        self.padding = (16, 8)
        self.font_size = 16
        self.bold = True
        
        # Bind events
        self.bind(on_press=self.animate_press)
        self.bind(on_release=self.animate_release)
    
    def animate_press(self, instance):
        """Animation when button is pressed"""
        anim = Animation(opacity=0.8, duration=0.1)
        anim.start(self)
    
    def animate_release(self, instance):
        """Animation when button is released"""
        anim = Animation(opacity=1.0, duration=0.15)
        anim.start(self)

class DiceButton(Button):
    """Specialized button for dice selection"""
    
    dice_type = NumericProperty(0)  # Number of sides
    bg_color = ListProperty([0.831, 0.686, 0.216, 1])  # #D4AF37
    text_color = ListProperty([0.173, 0.243, 0.314, 1])  # #2C3E50
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.bg_color
        self.color = self.text_color
        self.size_hint = (None, None)
        self.width = 56
        self.height = 56
        self.font_size = 16
        self.bold = True
        
        # Bind events
        self.bind(on_press=self.animate_press)
        self.bind(on_release=self.animate_release)
    
    def animate_press(self, instance):
        """Animation when button is pressed"""
        anim = Animation(opacity=0.8, duration=0.1)
        anim.start(self)
    
    def animate_release(self, instance):
        """Animation when button is released"""
        anim = Animation(opacity=1.0, duration=0.15)
        anim.start(self)