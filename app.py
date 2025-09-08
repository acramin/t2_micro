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

# Import screens
from screens.main_screen import MainScreen
from screens.profile_screen import ProfileScreen
from screens.profile_editor import ProfileEditorScreen
from screens.roll_screen import RollScreen, RollManager

# from screens.roll_screen import RollScreen

# Import custom components (needed for KV files)
from components.buttons import PrimaryButton, DiceButton

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
    
    def build(self):
        """Build the application"""
        self.title = "D&D Dice Roller"
        
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
    
    def load_profiles(self):
        """Load character profiles from JSON files"""
        # For now, create a sample profile with weapons
        self.current_profile = {
            'name': 'Sample Character',
            'level': 5,
            'abilities': {
                'STR': 16,
                'DEX': 14,
                'CON': 15,
                'INT': 10,
                'WIS': 12,
                'CHA': 8
            },
            'weapons': [
                {
                    'name': 'Longsword',
                    'ability': 'STR',
                    'proficient': True,
                    'damage_dice': '1d8',
                    'damage_bonus': 3,  # STR modifier
                    'damage_type': 'slashing'
                },
                {
                    'name': 'Shortbow',
                    'ability': 'DEX',
                    'proficient': True,
                    'damage_dice': '1d6',
                    'damage_bonus': 2,  # DEX modifier
                    'damage_type': 'piercing'
                },
                {
                    'name': 'Dagger',
                    'ability': 'DEX',
                    'proficient': True,
                    'damage_dice': '1d4',
                    'damage_bonus': 2,  # DEX modifier
                    'damage_type': 'piercing'
                }
            ],
            'saving_throw_proficiencies': ['STR', 'CON']  # For saving throws
        }
    
    def on_start(self):
        """Actions to perform when app starts"""
        # Set background color
        Window.clearcolor = (0.173, 0.243, 0.314, 1)  # #2C3E50
        
    def on_stop(self):
        """Actions to perform when app closes"""
        # Save any pending changes
        pass

if __name__ == '__main__':
    DnDDiceRollerApp().run()