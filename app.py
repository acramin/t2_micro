# app.py
"""
Main application class for D&D Dice Roller
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.properties import ObjectProperty, DictProperty
from kivy.lang import Builder
from kivy.config import Config
import os

# Disable multitouch emulation (red circles on right-click)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Enable virtual keyboard for touchscreens
# This makes the on-screen keyboard appear when text inputs are focused
# IMPORTANT: This must be set BEFORE any other Kivy imports that initialize the Window
Config.set('kivy', 'keyboard_mode', 'systemanddock')
# Alternative options:
# 'system' - uses system keyboard only (default on mobile)
# 'dock' - uses Kivy's virtual keyboard docked at bottom
# 'systemanddock' - shows both (best for Pi touchscreen - shows keyboard when TextInput is focused)
# '' or 'multi' - allows both modes

# Configure keyboard layout and behavior
Config.set('kivy', 'keyboard_layout', 'qwerty')  # Use standard QWERTY layout

# Note: If the keyboard still doesn't appear on first run, it may be due to cached config.
# To reset: Delete ~/.kivy/config.ini and restart the app

# Pi-specific image provider configuration
import platform
if 'arm' in platform.machine().lower() or 'raspberry' in platform.node().lower():
    # Force specific image provider for Pi compatibility
    from kivy.core.image import Image as CoreImage
    try:
        # Try to use PIL provider for better PNG support on Pi
        Config.set('image', 'providers', 'img_pil,img_tex,img_dds,img_sdl2')
    except:
        pass


# # Set window size to 800x480
# Config.set('graphics', 'width', '800')
# Config.set('graphics', 'height', '480')

# Enable fullscreen mode
Config.set('graphics', 'fullscreen', '1')
Config.set('graphics', 'width', '0')  # Use screen width
Config.set('graphics', 'height', '0')  # Use screen height
Config.set('graphics', 'resizable', False)

# Import screens
from screens.main_screen import MainScreen
from screens.profile_screen import ProfileScreen
from screens.profile_editor import ProfileEditorScreen
from screens.roll_screen import RollScreen, RollManager

# from screens.roll_screen import RollScreen

# Import custom components (needed for KV files)
from components.buttons import PrimaryButton, DiceButton

# Set window size explicitly after imports
Window.size = (800, 480)

# Load KV language files from the kv directory
kv_path = os.path.join(os.path.dirname(__file__), 'kv')
Builder.load_file(os.path.join(kv_path, 'main_screen.kv'))
Builder.load_file(os.path.join(kv_path, 'profile_screen.kv'))
Builder.load_file(os.path.join(kv_path, 'profile_editor.kv'))
Builder.load_file(os.path.join(kv_path, 'roll_screen.kv'))


class DnDDiceRollerApp(App):
    """Main application class"""
    
    # Properties
    screen_manager = ObjectProperty(None)
    current_profile = DictProperty(None, allownone=True)
    roll_manager = ObjectProperty(None)
    current_language = 'en'  # Default to English
    
    # Language translations
    translations = {
        'en': {
            'title': 'D&D Dice Roller',
            'current_character': 'Current Character: ',
            'change': 'Change',
            'attack': 'Attack',
            'saving_throw': 'Saving Throw',
            'ability_check': 'Ability Check',
            'custom': 'Custom',
            'exit': 'Exit',
            'language_button': 'PT-BR'
        },
        'pt': {
            'title': 'Rolador de Dados D&D',
            'current_character': 'Personagem Atual: ',
            'change': 'Mudar',
            'attack': 'Ataque',
            'saving_throw': 'Teste de Resistência',
            'ability_check': 'Teste de Habilidade',
            'custom': 'Personalizado',
            'exit': 'Sair',
            'language_button': 'EN-US'
        }
    }
    
    def build(self):
        """Build the application"""
        self.title = self.get_text('title')
        
        # Initialize screen manager
        self.screen_manager = ScreenManager(transition=FadeTransition())
        
        # Add screens
        self.screen_manager.add_widget(MainScreen(name='main'))
        self.screen_manager.add_widget(ProfileScreen(name='profiles'))
        self.screen_manager.add_widget(ProfileEditorScreen(name='profile_editor'))
        self.screen_manager.add_widget(RollScreen(name='roll'))
        self.roll_manager = RollManager(self)
        # Load initial data
        self.load_profiles()
        
        return self.screen_manager
    
    def get_text(self, key):
        """Get translated text for the current language"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def toggle_language(self):
        """Toggle between English and Portuguese"""
        self.current_language = 'pt' if self.current_language == 'en' else 'en'
        self.title = self.get_text('title')
        
        # Update the language button text in the main screen
        main_screen = self.screen_manager.get_screen('main')
        if hasattr(main_screen, 'ids'):
            # Force refresh of the screen content
            main_screen.on_enter()
    
    def load_profiles(self):
        """Load character profiles from JSON files"""
        from utils.file_utils import get_character_files, load_character_profile
        
        # Get list of saved character files
        character_files = get_character_files()
        
        if character_files:
            # Load the first character as current profile
            first_character = character_files[0].replace('.json', '')
            self.current_profile = load_character_profile(first_character)
        else:
            # No saved profiles, create a default one
            self.current_profile = {
                'name': 'Default Character',
                'level': 1,
                'abilities': {
                    'STR': 10,
                    'DEX': 10,
                    'CON': 10,
                    'INT': 10,
                    'WIS': 10,
                    'CHA': 10
                },
                'weapons': [],
                'saving_throw_proficiencies': []
            }
    
    def on_start(self):
        """Actions to perform when app starts"""
        # Set background color - Black
        Window.clearcolor = (0.0, 0.0, 0.0, 1)  # #000000
        
        # Programmatically set fullscreen mode
        try:
            Window.fullscreen = 'auto'  # Use 'auto' for best compatibility
        except Exception as e:
            # Fallback: maximize window if fullscreen fails
            try:
                Window.maximize()
            except:
                pass
        
    def on_stop(self):
        """Actions to perform when app closes"""
        # Save any pending changes
        pass

if __name__ == '__main__':
    DnDDiceRollerApp().run()