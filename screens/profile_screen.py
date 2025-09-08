# screens/profile_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from components.buttons import PrimaryButton
import os
import json

# screens/profile_screen.py (update ProfileButton)
class ProfileButton(BoxLayout):
    """Custom button for profile selection with edit option"""
    profile_data = ObjectProperty(None)
    
    def __init__(self, profile_data, **kwargs):
        super().__init__(**kwargs)
        self.profile_data = profile_data
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60
        self.spacing = 8
        
        # Profile name button
        profile_btn = Button(
            text=profile_data.get('name', 'Unnamed Character'),
            background_normal='',
            background_color=(0.44, 0.50, 0.56, 1),
            size_hint_x=0.5  # Reduced from 0.7 to make room for delete button
        )
        profile_btn.bind(on_press=self.select_profile)
        
        # Edit button
        edit_btn = Button(
            text="Edit",
            background_normal='',
            background_color=(0.541, 0.169, 0.886, 1),
            size_hint_x=0.25  # Reduced from 0.3
        )
        edit_btn.bind(on_press=self.edit_profile)
        
        # Delete button
        delete_btn = Button(
            text="Delete",
            background_normal='',
            background_color=(0.906, 0.298, 0.235, 1),  # Red color
            size_hint_x=0.25  # New delete button
        )
        delete_btn.bind(on_press=self.delete_profile)
        
        self.add_widget(profile_btn)
        self.add_widget(edit_btn)
        self.add_widget(delete_btn)
    
    def select_profile(self, instance):
        """Select a profile and return to main screen"""
        self.parent.parent.parent.parent.select_profile(self.profile_data)
    
    def edit_profile(self, instance):
        """Edit this profile"""
        self.parent.parent.parent.parent.edit_profile(self.profile_data)
    
    def delete_profile(self, instance):
        """Delete this profile"""
        self.parent.parent.parent.parent.delete_profile(self.profile_data)

class ProfileScreen(Screen):
    """Screen for managing character profiles"""
    
    profiles_layout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        
    def on_enter(self):
        """Called when the screen is displayed"""
        # Get reference to the app instance
        if not self.app:
            from kivy.app import App
            self.app = App.get_running_app()
        
        # Load and display profiles
        self.load_profiles()
    
    def load_profiles(self):
        """Load and display all character profiles"""
        # Clear existing profiles
        if self.ids.get('profiles_container'):
            self.ids.profiles_container.clear_widgets()
        
        # Get profiles from data directory
        profiles = self.get_profile_files()
        
        # Add create new profile button
        create_btn = PrimaryButton(
            text="Create New Profile",
            size_hint_y=None,
            height=60
        )
        create_btn.bind(on_press=self.create_new_profile)
        
        if self.ids.get('profiles_container'):
            self.ids.profiles_container.add_widget(create_btn)
        
        # Add profile buttons
        for profile_file in profiles:
            profile_data = self.load_profile(profile_file)
            if profile_data:
                profile_btn = ProfileButton(
                    profile_data=profile_data,
                    size_hint_y=None,
                    height=60
                )
                profile_btn.bind(on_press=self.select_profile)
                
                if self.ids.get('profiles_container'):
                    self.ids.profiles_container.add_widget(profile_btn)
    
    def get_profile_files(self):
        """Get list of profile files"""
        profiles_path = os.path.join('data', 'characters')
        if not os.path.exists(profiles_path):
            os.makedirs(profiles_path)
            return []
        
        return [f for f in os.listdir(profiles_path) if f.endswith('.json')]
    
    def load_profile(self, filename):
        """Load a profile from file"""
        try:
            profiles_path = os.path.join('data', 'characters')
            filepath = os.path.join(profiles_path, filename)
            with open(filepath, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            return None
    
    def select_profile(self, profile_data):
        """Select a profile and return to main screen"""
        self.app.current_profile = profile_data
        self.app.screen_manager.current = 'main'
    def edit_profile(self, profile_data):
        """Edit a profile"""
        self.app.current_profile = profile_data
        self.app.screen_manager.current = 'profile_editor'

    def create_new_profile(self, instance):
        """Create a new profile"""
        # Clear current profile to indicate new profile
        self.app.current_profile = None
        self.app.screen_manager.current = 'profile_editor'

    def save_profile(self, profile_data):
        """Save a profile to file"""
        try:
            profiles_path = os.path.join('data', 'characters')
            if not os.path.exists(profiles_path):
                os.makedirs(profiles_path)
            
            # Create a safe filename
            safe_name = "".join(c for c in profile_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_name}.json"
            filepath = os.path.join(profiles_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(profile_data, f, indent=4)
            
            return True
        except IOError:
            return False
    
    def delete_profile(self, profile_data):
        """Delete a profile file"""
        try:
            profiles_path = os.path.join('data', 'characters')
            
            # Create the same safe filename as when saving
            safe_name = "".join(c for c in profile_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_name}.json"
            filepath = os.path.join(profiles_path, filename)
            
            # Remove the file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # If this was the currently selected profile, clear it
            if self.app.current_profile and self.app.current_profile.get('name') == profile_data.get('name'):
                self.app.current_profile = None
            
            # Refresh the profile list
            self.load_profiles()
            
            return True
        except IOError:
            return False
    
    def back_to_main(self):
        """Return to the main screen"""
        self.app.screen_manager.current = 'main'