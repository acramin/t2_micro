"""
Main application class for D&D Dice Roller
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import os

# Import screens (to be implemented in future steps)
# from screens.main_screen import MainScreen
# from screens.profile_screen import ProfileScreen
# from screens.roll_screen import RollScreen

# Load KV language files from the kv directory
kv_path = os.path.join(os.path.dirname(__file__), 'kv')
Builder.load_file(os.path.join(kv_path, 'main_screen.kv'))
Builder.load_file(os.path.join(kv_path, 'profile_screen.kv'))
Builder.load_file(os.path.join(kv_path, 'roll_screen.kv'))

def create_data_directories():
    """Create the necessary data directories"""
    directories = [
        'data',
        'data/characters',
        'data/backups',
        'data/animations'
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
            
class DnDDiceRollerApp(App):
    """Main application class"""
    
    # Properties
    screen_manager = ObjectProperty(None)
    current_profile = ObjectProperty(None, allownone=True)
    
    def build(self):
        """Build the application"""
        self.title = "D&D Dice Roller"
        
        # Initialize screen manager
        self.screen_manager = ScreenManager(transition=FadeTransition())
        
        # Add screens (to be implemented)
        # self.screen_manager.add_widget(MainScreen(name='main'))
        # self.screen_manager.add_widget(ProfileScreen(name='profiles'))
        # self.screen_manager.add_widget(RollScreen(name='roll'))
        
        # Load initial data
        self.load_profiles()
        
        return self.screen_manager
    
    def load_profiles(self):
        """Load character profiles from JSON files"""
        # To be implemented in file_utils.py
        pass
    
    def on_start(self):
        """Actions to perform when app starts"""
        # Set background color
        Window.clearcolor = (0.173, 0.243, 0.314, 1)  # #2C3E50
        
    def on_stop(self):
        """Actions to perform when app closes"""
        # Save any pending changes
        pass





if __name__ == '__main__':
    create_data_directories()
    DnDDiceRollerApp().run()