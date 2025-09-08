# screens/main_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock

class MainScreen(Screen):
    """Main screen with dice rolling interface"""
    
    # Properties
    current_character = StringProperty("None")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def on_enter(self):
        """Called when the screen is displayed"""
        # Get reference to the app instance
        if not self.app:
            from kivy.app import App
            self.app = App.get_running_app()
            
        # Update current character display
        if self.app.current_profile:
            self.current_character = self.app.current_profile.get('name', 'Unknown')
        else:
            self.current_character = "None"
    
    def initiate_attack_roll(self):
        """Initiate an attack roll"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_weapon_dialog()

    def initiate_saving_throw(self):
        """Initiate a saving throw"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_ability_dialog("saving_throw")

    def initiate_ability_check(self):
        """Initiate an ability check"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_ability_dialog("ability_check")

    def show_custom_dice_dialog(self):
        """Show custom dice dialog"""
        if self.app and self.app.roll_manager:
            self.app.roll_manager.show_custom_dice_dialog()

    def roll_dice(self, sides):
        """Roll a specific die"""
        print(f"Rolling d{sides}")
        if self.app and self.app.roll_manager:
            self.app.roll_manager.roll_dice(sides)