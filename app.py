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

# Set window size to 800x480
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
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
        print(f"Language changed to: {'Portuguese' if self.current_language == 'pt' else 'English'}")
        
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
            print(f"Loaded profile: {self.current_profile.get('name', 'Unknown')}")
        else:
            # No saved profiles, create a default one
            print("No saved profiles found, creating default profile")
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
        
    def on_stop(self):
        """Actions to perform when app closes"""
        # Save any pending changes
        pass

if __name__ == '__main__':
    DnDDiceRollerApp().run()