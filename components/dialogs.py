# components/dialogs.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from components.buttons import PrimaryButton

class SelectionDialog(ModalView):
    """Base class for selection dialogs"""
    
    def __init__(self, title, options, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.options = options
        self.selected_option = None
        self.size_hint = (0.8, 0.8)
        self.auto_dismiss = False
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title_label = Label(
            text=self.title,
            size_hint_y=None,
            height=40,
            font_size=20,
            bold=True
        )
        layout.add_widget(title_label)
        
        # Options grid
        options_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.8)
        for option in self.options:
            btn = PrimaryButton(
                text=str(option),
                size_hint_y=None,
                height=60
            )
            btn.bind(on_press=lambda instance, opt=option: self.select_option(opt))
            options_grid.add_widget(btn)
        layout.add_widget(options_grid)
        
        # Cancel button
        cancel_btn = Button(
            text="Cancel",
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_press=self.dismiss)
        layout.add_widget(cancel_btn)
        
        self.add_widget(layout)
    
    def select_option(self, option):
        """Handle option selection"""
        self.selected_option = option
        self.dismiss()

class AbilityDialog(SelectionDialog):
    """Dialog for selecting an ability"""
    
    def __init__(self, **kwargs):
        abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        super().__init__("Select Ability", abilities, **kwargs)

class ComprehensiveAbilityDialog(ModalView):
    """Comprehensive dialog for selecting abilities and skills with scrolling"""
    
    def __init__(self, profile_data=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Select Ability or Skill"
        self.selected_option = None
        self.size_hint = (0.9, 0.9)
        self.auto_dismiss = False
        self.profile_data = profile_data or {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the comprehensive dialog UI"""
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title_label = Label(
            text=self.title,
            size_hint_y=None,
            height=40,
            font_size=20,
            bold=True
        )
        layout.add_widget(title_label)
        
        # Scrollable content
        scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=False, do_scroll_y=True)
        
        # Content layout for scrollable area
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Basic Abilities section
        abilities_label = Label(
            text="Basic Abilities",
            size_hint_y=None,
            height=30,
            font_size=16,
            bold=True,
            color=(0.2, 0.6, 0.8, 1)
        )
        content_layout.add_widget(abilities_label)
        
        # Basic abilities
        basic_abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for ability in basic_abilities:
            ability_score = self.profile_data.get('abilities', {}).get(ability, 10)
            ability_mod = (ability_score - 10) // 2
            
            btn = PrimaryButton(
                text=f"{ability} (Modifier: {ability_mod:+d})",
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=lambda instance, opt=ability: self.select_option(opt))
            content_layout.add_widget(btn)
        
        # Skills section
        skills_label = Label(
            text="Skills",
            size_hint_y=None,
            height=30,
            font_size=16,
            bold=True,
            color=(0.8, 0.6, 0.2, 1)
        )
        content_layout.add_widget(skills_label)
        
        # Skills with their associated abilities
        skills_data = [
            ("Acrobatics", "DEX"),
            ("Animal Handling", "WIS"),
            ("Arcana", "INT"),
            ("Athletics", "STR"),
            ("Deception", "CHA"),
            ("History", "INT"),
            ("Insight", "WIS"),
            ("Intimidation", "CHA"),
            ("Investigation", "INT"),
            ("Medicine", "WIS"),
            ("Nature", "INT"),
            ("Perception", "WIS"),
            ("Performance", "CHA"),
            ("Persuasion", "CHA"),
            ("Religion", "INT"),
            ("Sleight of Hand", "DEX"),
            ("Stealth", "DEX"),
            ("Survival", "WIS")
        ]
        
        skill_proficiencies = self.profile_data.get('skill_proficiencies', [])
        level = self.profile_data.get('level', 1)
        prof_bonus = self.calculate_proficiency_bonus(level)
        
        for skill_name, skill_ability in skills_data:
            ability_score = self.profile_data.get('abilities', {}).get(skill_ability, 10)
            ability_mod = (ability_score - 10) // 2
            is_proficient = skill_name in skill_proficiencies
            
            total_mod = ability_mod + (prof_bonus if is_proficient else 0)
            prof_text = " (Proficient)" if is_proficient else ""
            
            btn = PrimaryButton(
                text=f"{skill_name} ({skill_ability}) - Modifier: {total_mod:+d}{prof_text}",
                size_hint_y=None,
                height=45,
                font_size=14
            )
            btn.bind(on_press=lambda instance, opt=skill_name: self.select_option(opt))
            content_layout.add_widget(btn)
        
        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)
        
        # Cancel button
        cancel_btn = Button(
            text="Cancel",
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        cancel_btn.bind(on_press=self.dismiss)
        layout.add_widget(cancel_btn)
        
        self.add_widget(layout)
    
    def calculate_proficiency_bonus(self, level):
        """Calculate proficiency bonus based on level"""
        if level < 5:
            return 2
        elif level < 9:
            return 3
        elif level < 13:
            return 4
        elif level < 17:
            return 5
        else:
            return 6
    
    def select_option(self, option):
        """Handle option selection"""
        self.selected_option = option
        self.dismiss()

class WeaponDialog(SelectionDialog):
    """Dialog for selecting a weapon"""
    
    def __init__(self, weapons, **kwargs):
        weapon_names = [weapon.get('name', f'Weapon {i+1}') for i, weapon in enumerate(weapons)]
        super().__init__("Select Weapon", weapon_names, **kwargs)

class DiceDialog(SelectionDialog):
    """Dialog for custom dice rolls"""
    
    def __init__(self, **kwargs):
        dice_options = [
            "d4", "d6", "d8", "d10", "d12", "d20", "d100",
            "2d4", "2d6", "2d8", "2d10", "3d4", "3d6", "3d8",
            "4d4", "4d6", "4d8", "Custom"
        ]
        super().__init__("Select Dice", dice_options, **kwargs)