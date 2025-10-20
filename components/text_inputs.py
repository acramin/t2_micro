"""Custom TextInput widgets with persistent keyboard support"""

from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class PersistentKeyboardTextInput(TextInput):
    """TextInput that keeps keyboard visible once opened"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard_shown = False
        
    def on_touch_down(self, touch):
        """Handle touch to show keyboard"""
        if self.collide_point(*touch.pos):
            # Give focus to this input
            self.focus = True
            self._keyboard_shown = True
            # Let the normal touch handling proceed
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)
    
    def on_focus(self, instance, value):
        """Handle focus changes"""
        if value:
            # When focused, ensure keyboard is requested
            self._keyboard_shown = True
            # Schedule keyboard request slightly delayed
            Clock.schedule_once(lambda dt: self._request_keyboard(), 0.05)
        # Don't automatically hide keyboard on focus loss
        # User must explicitly move to another field or tap outside
    
    def _request_keyboard(self):
        """Request keyboard display"""
        if self.focus and not self._keyboard:
            self._ensure_keyboard()
    
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Override to prevent keyboard from hiding on certain keys"""
        # Call parent implementation
        super().keyboard_on_key_down(window, keycode, text, modifiers)
        
        # Keep keyboard visible
        if not self.focus:
            self.focus = True
