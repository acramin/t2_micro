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