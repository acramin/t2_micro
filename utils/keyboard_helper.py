"""Helper module to manage persistent virtual keyboard behavior"""

from kivy.core.window import Window
from kivy.clock import Clock


class KeyboardHelper:
    """Helper class to manage virtual keyboard persistence"""
    
    _instance = None
    _keyboard_visible = False
    _active_textinput = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyboardHelper, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._setup_keyboard()
    
    def _setup_keyboard(self):
        """Set up keyboard event listeners"""
        Window.bind(on_keyboard=self._on_keyboard)
    
    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle keyboard events to prevent auto-hide"""
        # Return False to allow normal keyboard processing
        return False
    
    def show_keyboard(self, textinput):
        """Show keyboard for a specific TextInput"""
        if textinput is None:
            return
        
        self._active_textinput = textinput
        
        # Ensure TextInput has focus
        if not textinput.focus:
            textinput.focus = True
        
        # Request keyboard display
        Clock.schedule_once(lambda dt: self._ensure_keyboard_visible(textinput), 0.1)
        self._keyboard_visible = True
    
    def _ensure_keyboard_visible(self, textinput):
        """Ensure the keyboard is actually visible"""
        if textinput and hasattr(textinput, '_keyboard'):
            # The keyboard should already be shown by focus
            pass
        # Force focus again if needed
        if textinput and not textinput.focus:
            textinput.focus = True
    
    def hide_keyboard(self):
        """Hide the keyboard (only call explicitly when needed)"""
        if self._active_textinput:
            self._active_textinput.focus = False
            self._active_textinput = None
        self._keyboard_visible = False
    
    def is_keyboard_visible(self):
        """Check if keyboard is currently visible"""
        return self._keyboard_visible


# Global instance
keyboard_helper = KeyboardHelper()
