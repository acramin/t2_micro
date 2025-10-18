# screens/profile_editor.py
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from components.buttons import PrimaryButton
from utils.calculations import calculate_modifier, calculate_proficiency_bonus, validate_ability_score
import json
import os

class AbilityInput(BoxLayout):
    """Widget for ability score input with modifier display"""
    ability_name = StringProperty("")
    ability_value = NumericProperty(10)
    ability_modifier = NumericProperty(0)
    
    def __init__(self, ability_name="", ability_value=10, **kwargs):
        super().__init__(**kwargs)
        self.ability_name = ability_name
        self.ability_value = ability_value
        self.update_modifier()
    
    def update_value(self, value):
        """Update the ability value and recalculate modifier"""
        try:
            self.ability_value = validate_ability_score(int(value))
            self.update_modifier()
        except ValueError:
            pass
    
    def update_modifier(self):
        """Calculate and update the modifier display"""
        self.ability_modifier = calculate_modifier(self.ability_value)
    
    def increase_value(self):
        """Increase the ability value by 1"""
        self.ability_value = validate_ability_score(self.ability_value + 1)
        self.update_modifier()
        # Update the text input display
        self.ids.ability_value_input.text = str(self.ability_value)
    
    def decrease_value(self):
        """Decrease the ability value by 1"""
        self.ability_value = validate_ability_score(self.ability_value - 1)
        self.update_modifier()
        # Update the text input display
        self.ids.ability_value_input.text = str(self.ability_value)

class SkillCheckbox(BoxLayout):
    """Widget for skill proficiency checkbox"""
    skill_name = StringProperty("")
    is_proficient = ObjectProperty(False)
    ability = StringProperty("")

class WeaponInput(BoxLayout):
    """Widget for weapon input"""
    weapon_name = StringProperty("")
    weapon_ability = StringProperty("STR")
    weapon_damage_dice = StringProperty("d6")
    weapon_damage_bonus = NumericProperty(0)
    weapon_proficient = ObjectProperty(True)

class ProfileEditorScreen(Screen):
    """Screen for editing character profiles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
        self.profile_data = None
        self.is_new_profile = False
    
    def on_enter(self):
        """Called when the screen is displayed"""
        # Get reference to the app instance
        if not self.app:
            from kivy.app import App
            self.app = App.get_running_app()
        
        # Load profile data if editing existing profile
        if self.app.current_profile:
            self.profile_data = self.app.current_profile.copy()
            self.is_new_profile = False
        else:
            # Create new profile data structure
            self.profile_data = {
                "name": "New Character",
                "level": 1,
                "abilities": {
                    "STR": 10, "DEX": 10, "CON": 10,
                    "INT": 10, "WIS": 10, "CHA": 10
                },
                "saving_throw_proficiencies": [],
                "skill_proficiencies": [],
                "weapons": []
            }
            self.is_new_profile = True
        
        # Populate the form with profile data
        self.populate_form()
    
    def populate_form(self):
        """Populate the form with profile data"""
        # Basic info
        if self.ids.get('character_name'):
            self.ids.character_name.text = self.profile_data.get('name', '')
        
        if self.ids.get('character_level'):
            self.ids.character_level.text = str(self.profile_data.get('level', 1))
        
        # Ability scores
        abilities = self.profile_data.get('abilities', {})
        for ability, value in abilities.items():
            ability_id = f'ability_{ability.lower()}'
            if self.ids.get(ability_id):
                ability_input = self.ids[ability_id]
                ability_input.ability_value = value
                # Also update the text input display
                if hasattr(ability_input, 'ids') and 'ability_value_input' in ability_input.ids:
                    ability_input.ids.ability_value_input.text = str(value)
        
        # Saving throw proficiencies
        saving_throws = self.profile_data.get('saving_throw_proficiencies', [])
        for ability in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            if self.ids.get(f'save_{ability.lower()}'):
                self.ids[f'save_{ability.lower()}'].active = ability in saving_throws
        
        # Skill proficiencies
        skills = self.profile_data.get('skill_proficiencies', [])
        for skill in self.get_skill_list():
            skill_id = skill.lower().replace(' ', '_')
            widget_id = f'skill_{skill_id}'
            if self.ids.get(widget_id):
                is_in_profile = skill in skills
                self.ids[widget_id].ids.checkbox.active = is_in_profile
        
        # Weapons
        if self.ids.get('weapons_container'):
            self.ids.weapons_container.clear_widgets()
            
            weapons = self.profile_data.get('weapons', [])
            for weapon in weapons:
                self.add_weapon_input(weapon)
    
    def get_skill_list(self):
        """Return list of all skills"""
        return [
            "Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception",
            "History", "Insight", "Intimidation", "Investigation", "Medicine",
            "Nature", "Perception", "Performance", "Persuasion", "Religion",
            "Sleight of Hand", "Stealth", "Survival"
        ]
    
    def add_weapon_input(self, weapon_data=None):
        """Add a weapon input widget"""
        if not weapon_data:
            weapon_data = {
                "name": "New Weapon",
                "ability": "STR",
                "damage_dice": "d6",
                "damage_bonus": 0,
                "proficient": True
            }
        
        weapon_input = WeaponInput(
            weapon_name=weapon_data.get('name', ''),
            weapon_ability=weapon_data.get('ability', 'STR'),
            weapon_damage_dice=weapon_data.get('damage_dice', 'd6'),
            weapon_damage_bonus=weapon_data.get('damage_bonus', 0),
            weapon_proficient=weapon_data.get('proficient', True),
            size_hint_y=None,
            height=100
        )
        
        if self.ids.get('weapons_container'):
            self.ids.weapons_container.add_widget(weapon_input)
    
    def remove_weapon_input(self, instance):
        """Remove a weapon input widget"""
        if self.ids.get('weapons_container'):
            self.ids.weapons_container.remove_widget(instance)
    
    def save_profile(self):
        """Save the profile data"""
        # Basic info
        self.profile_data['name'] = self.ids.character_name.text
        try:
            self.profile_data['level'] = int(self.ids.character_level.text)
        except ValueError:
            self.profile_data['level'] = 1
        
        # Ability scores
        for ability in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            ability_id = f'ability_{ability.lower()}'
            if self.ids.get(ability_id):
                ability_input = self.ids[ability_id]
                old_value = self.profile_data['abilities'].get(ability, 10)
                new_value = validate_ability_score(ability_input.ability_value)
                self.profile_data['abilities'][ability] = new_value
        
        # Saving throw proficiencies
        self.profile_data['saving_throw_proficiencies'] = []
        for ability in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            if self.ids[f'save_{ability.lower()}'].active:
                self.profile_data['saving_throw_proficiencies'].append(ability)
        
        # Skill proficiencies
        self.profile_data['skill_proficiencies'] = []
        for skill in self.get_skill_list():
            skill_id = skill.lower().replace(' ', '_')
            widget_id = f'skill_{skill_id}'
            if self.ids.get(widget_id):
                is_active = self.ids[widget_id].ids.checkbox.active
                if is_active:
                    self.profile_data['skill_proficiencies'].append(skill)
        
        # Weapons
        self.profile_data['weapons'] = []
        if self.ids.get('weapons_container'):
            for child in self.ids.weapons_container.children:
                if isinstance(child, WeaponInput):
                    weapon_data = {
                        "name": child.weapon_name,
                        "ability": child.weapon_ability,
                        "damage_dice": child.weapon_damage_dice,
                        "damage_bonus": child.weapon_damage_bonus,
                        "proficient": child.weapon_proficient
                    }
                    self.profile_data['weapons'].append(weapon_data)
        
        # Save to file
        self.save_to_file()
        
        # Update app current profile
        self.app.current_profile = self.profile_data
        
        # Return to profile screen
        self.app.screen_manager.current = 'profiles'
    
    def save_to_file(self):
        """Save profile data to JSON file"""
        try:
            profiles_path = os.path.join('data', 'characters')
            if not os.path.exists(profiles_path):
                os.makedirs(profiles_path)
            
            # Create a safe filename
            safe_name = "".join(c for c in self.profile_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_name}.json"
            filepath = os.path.join(profiles_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(self.profile_data, f, indent=4)
            
            return True
        except IOError:
            return False
    
    def back_to_profiles(self):
        """Return to the profile screen without saving"""
        self.app.screen_manager.current = 'profiles'